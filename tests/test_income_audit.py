"""Regression cases for dividend entitlement, selected screen yield and action gates."""
import unittest

from scripts.validate_analysis import validate_report
from test_analysis_contract import full_report, EVIDENCE


def screen_report(target=.05):
    return {
        'mode': 'screen',
        'screening_parameters': {'target_net_yield': target,
            'target_basis': 'user_explicit' if target is not None else 'not_assessed',
            'target_policy': 'hard_minimum' if target is not None else 'not_assessed'},
        'screen_results': [{
            'company':'Synthetic', 'ticker':'TEST', 'exchange':'Example', 'as_of_date':'2026-01-01',
            'price_used':10, 'price_currency':'HKD', 'ttm_net_yield':.09,
            'screening_yield_used':.04, 'screening_yield_basis':'FY ordinary excluding one-off special; same currency; after tax before fees',
            'screening_yield_range':{'low':.04,'high':.04}, 'screening_basis_usable':True,
            'withholding_basis':'company_announcement', 'screening_net_yield_target':target,
            'yield_fit':'Below target' if target is not None else 'Not Assessed',
            'yield_gap_percentage_points':-1 if target is not None else None,
            'documented_dividend_growth_path':'Unclear', 'five_year_dps_pattern':'Stable',
            'latest_coverage':'1.5x', 'balance_sheet_alert':'None', 'withholding_efficiency':'High',
            'preliminary_fundamental_trend':'Stable', 'dividend_trap_screen':'Pass',
            'full_analysis_recommended':'No' if target is not None else 'Watch', 'main_reason':EVIDENCE,
            'forecast_confidence':'Not Assessed', 'buy_zone':'Not Assessed', 'sources':[EVIDENCE],
        }],
    }


class IncomeAuditTests(unittest.TestCase):
    def assertValid(self, report):
        self.assertEqual(validate_report(report), [])

    def assertInvalid(self, report, fragment):
        errors = validate_report(report)
        self.assertTrue(any(fragment in error for error in errors), '\n'.join(errors))

    def test_special_ttm_cannot_pass_recurring_hard_minimum(self):
        report=screen_report()
        self.assertValid(report)
        report['screen_results'][0].update(yield_fit='Pass', yield_gap_percentage_points=4, full_analysis_recommended='Yes')
        self.assertInvalid(report, 'selected yield range')

    def test_supported_tax_range_straddles_target(self):
        report=screen_report()
        row=report['screen_results'][0]
        row.update(screening_yield_used=None, screening_yield_range={'low':.045,'high':.055},
                   yield_fit='Unclear', yield_gap_percentage_points=None, full_analysis_recommended='Watch')
        self.assertValid(report)
        row.update(yield_fit='Pass', full_analysis_recommended='Yes')
        self.assertInvalid(report, 'selected yield range')

    def test_unusable_or_missing_yield_does_not_pass(self):
        report=screen_report()
        row=report['screen_results'][0]
        row.update(screening_yield_used=.08, screening_yield_range={'low':.08,'high':.08}, screening_basis_usable=False,
                   yield_fit='Unclear', yield_gap_percentage_points=None, full_analysis_recommended='Watch')
        self.assertValid(report)
        row['screening_yield_range']={'low':None,'high':None}
        row['screening_yield_used']=None
        self.assertValid(report)

    def test_no_target_has_no_invented_cutoff(self):
        self.assertValid(screen_report(None))

    def test_reversed_yield_range_is_rejected(self):
        report=screen_report()
        report['screen_results'][0]['screening_yield_range']={'low':.06,'high':.04}
        self.assertInvalid(report,'reversed')

    def test_scrip_cash_cost_does_not_reduce_cash_election_dps(self):
        for growth in (False,True):
            report=full_report(growth=growth)
            for row in report['dividend_and_yield_runway']:
                row['cash_settled_fraction']=.6
                row['dividend_cash_cost']=row['dividend_entitlement']*.6
            self.assertValid(report)
            report['dividend_and_yield_runway'][1]['derived_dps'] *= .6
            self.assertInvalid(report,'DPS')

    def test_broker_drip_does_not_retain_issuer_cash(self):
        report=full_report()
        row=report['dividend_and_yield_runway'][1]
        row['dividend_cash_cost'] *= .6  # Cash-settled fraction remains 1 for broker DRIP.
        self.assertInvalid(report,'issuer cash settlement')

    def test_multiple_entitlement_counts_aggregate_dps_separately(self):
        report=full_report()
        row=report['dividend_and_yield_runway'][1]
        row['dividend_installments']=[{
            'record_date':date, 'dividend_entitled_shares':shares, 'dividend_entitlement':20,
            'cash_settled_fraction':1, 'settlement_cash_adjustment':0,
            'derived_dps':20/shares, 'dividend_cash_cost':20,
        } for date,shares in [('2026-06-01',10),('2026-12-01',12)]]
        row['derived_dps']=2+20/12
        row['dividend_entitled_shares']=40/row['derived_dps']
        row['share_count_reconciliation']='Dividend-weighted annual count; actual record-date counts 10 and 12.'
        self.assertValid(report)
        row['derived_dps']=40/12
        self.assertInvalid(report,'annual DPS')

    def test_scrip_cannot_hide_unfunded_growth_entitlement(self):
        report=full_report(growth=True)
        row=report['dividend_and_yield_runway'][1]
        row.update(dividend_entitlement=80, dividend_cash_cost=48, cash_settled_fraction=.6,
                   derived_dps=8, all_cash_funding_gap=10,
                   policy_adjustment_reason='Synthetic larger payout; not supported by recurring FAD 75 or actual capacity 70.')
        self.assertInvalid(report,'growth requires funded')

    def test_terminal_scrip_does_not_reduce_cash_option_value(self):
        report=full_report(growth=True)
        for scenario in report['growth_valuation']['scenarios']:
            funding=scenario['terminal_funding']
            funding['cash_settled_fraction']=.6
            funding['dividend_cash_cost']=funding['dividend_entitlement']*.6
        self.assertValid(report)
        report['growth_valuation']['scenarios'][0]['terminal_funding']['dividend_entitlement']=1
        self.assertInvalid(report,'issuer cash settlement')

    def test_strong_buy_requires_high_safety_and_price_gates(self):
        report=full_report()
        report['price_used']=30
        report['income_assessment']['forward_net_yield']=4/30
        report['forecast_confidence']='High'
        report['cash_flow_model']['evidence_status']='reported_reconciled'
        report['dividend_safety']='Strong'
        report['action_assessment']['strong_buy_eligible']=True
        self.assertValid(report)
        report['forecast_confidence']='Medium'
        self.assertInvalid(report,'High')
        report['forecast_confidence']='High'
        report['dividend_safety']='Acceptable'
        self.assertInvalid(report,'Strong')

    def test_low_confidence_only_supports_diagnostic_action(self):
        report=full_report()
        report['forecast_confidence']='Low'
        self.assertInvalid(report,'Low confidence')
        report['action_assessment']['status']='diagnostic_only'
        self.assertValid(report)

    def test_bad_schema_version_is_rejected(self):
        report=full_report()
        report['schema_version']='999'
        self.assertInvalid(report,'2.1')

    def test_finite_life_pv_must_reconcile(self):
        report=full_report()
        report.pop('buy_zone')
        report.update(valuation_mode='finite_life_harvest', fundamental_trend='Structural Decline',
                      structural_decline_cap_applied=True, harvest_managed_runoff_exception_applied=True,
                      grade='C', portfolio_role='Opportunistic')
        report['key_metrics_at_a_glance'].update(valuation_mode='finite_life_harvest', grade='C', portfolio_role='Opportunistic')
        pv=10/1.1+10/1.1**2
        report['finite_life_valuation']={
            'harvest_horizon_years':2, 'discount_rate':.1,
            'forecast_net_distributions':[{'year':str(y), 'net_distribution':10, 'present_value':10/1.1**y} for y in [1,2]],
            'present_value_of_distributions':pv, 'residual_value':0, 'residual_value_basis':EVIDENCE,
            'finite_life_value_low':pv, 'finite_life_value_high':pv,
        }
        self.assertValid(report)
        report['finite_life_valuation']['forecast_net_distributions'][0]['present_value']=100
        self.assertInvalid(report,'Finite-life distribution PV')

    def test_bear_fallback_is_not_actionable_entry(self):
        report=full_report()
        report['buy_zone']['bear_net_dps_is_fallback']=True
        self.assertInvalid(report,'diagnostic only')
        report['action_assessment']['status']='diagnostic_only'
        self.assertValid(report)

if __name__=='__main__':
    unittest.main()
