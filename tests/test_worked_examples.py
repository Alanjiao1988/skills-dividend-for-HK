"""Worked-example tests from disk source; repository bundle builds are out of scope."""
import json
import unittest
from pathlib import Path
from scripts.validate_analysis import validate_report

ROOT = Path(__file__).resolve().parents[1]
if (ROOT / "dividend-income-equity-analysis").is_dir():
    ROOT /= "dividend-income-equity-analysis"

class WorkedExampleTests(unittest.TestCase):
    def load(self, mode):
        return json.loads((ROOT / f'examples\\{mode}.analysis.json').read_text(encoding='utf8'))

    def test_both_complete_records_validate(self):
        for mode in ('ordinary', 'growth'):
            self.assertEqual(validate_report(self.load(mode)), [])

    def test_cash_policy_and_income_answers(self):
        report = self.load('ordinary')
        row = next(x for x in report['dividend_and_yield_runway'] if x['forecast_year'] == 1 and x['scenario'] == 'Base')
        self.assertEqual((row['dividend_entitlement'], row['cash_available_for_distribution'], row['derived_dps']), (40, 70, 4))
        self.assertEqual(report['buy_zone']['boundaries']['too_expensive_above'], 50)
        self.assertEqual(report['buy_zone']['boundaries']['accumulation_upper'], 40)
        self.assertEqual(report['buy_zone']['boundaries']['strong_buy_at_or_below'], 32)
        self.assertFalse(report['action_assessment']['strong_buy_eligible'])

    def test_growth_cross_check_and_entry_answer(self):
        value = self.load('growth')['growth_valuation']
        expected = {'Bear': 45.7142857143, 'Base': 57.1428571429, 'Bull': 68.5714285714}
        for row in value['scenarios']:
            self.assertEqual(row['required_return'], .09)
            self.assertAlmostEqual(row['total_value'], expected[row['scenario']], places=8)
        self.assertAlmostEqual(value['entry_upper'], 38.8571428571, places=8)

    def test_examples_expose_scores_ratings_and_positive_entry(self):
        for mode in ('ordinary', 'growth'):
            report = self.load(mode)
            self.assertEqual(report['schema_version'], '3.0')
            self.assertEqual(report['scorecard']['rubric_version'], '2')
            self.assertEqual(report['scorecard']['quality_score_85'], 62)
            self.assertEqual(report['scorecard']['income_score_15'], 14)
            self.assertEqual(report['score_100'], 76)
            self.assertEqual(report['scorecard']['summary']['score_range'], {'low': 76, 'high': 76})
            self.assertEqual(report['scorecard']['summary']['status'], 'provisional')
            self.assertEqual(report['scorecard']['summary']['evidence_coverage_pct'], 100)
            self.assertEqual(report['entry_plan']['current_action'], 'accumulate')
            self.assertEqual(len(report['rating_audit']), 8)
            self.assertFalse(report['entry_plan']['automatic_trade'])

    def test_fixture_dividend_cannot_be_edited_without_funding_reconciliation(self):
        report = self.load('ordinary')
        report['dividend_and_yield_runway'][0]['derived_dps'] += 1
        self.assertTrue(validate_report(report))
