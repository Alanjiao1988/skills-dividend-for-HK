"""Normalization evidence completeness and action consistency, not source truth."""

import unittest

from scripts.validate_analysis import validate_report
from test_analysis_contract import EVIDENCE, full_report


def mark_operating_gap(report, status="missing"):
    report["buy_zone"]["normalization_evidence"]["operating_cash"].update(
        status=status,
        input_detail="No volume, margin or working-capital reconciliation supports the illustrative Base cash path.",
        source_refs=[EVIDENCE] if status == "conflicting" else [],
        resolution_source="Segment guidance and annual-report cash-flow/working-capital notes",
        consequence="The normalized DPS is diagnostic, not an evidenced entry input.",
    )
    report["action_assessment"].update(status="diagnostic_only", strong_buy_eligible=False)


class NormalizationEvidenceTests(unittest.TestCase):
    def assertValid(self, report):
        self.assertEqual(validate_report(report), [])

    def assertInvalid(self, report, fragment):
        errors = validate_report(report)
        self.assertTrue(any(fragment in error for error in errors), "\n".join(errors))

    def test_supported_links_preserve_existing_valuation(self):
        for growth in (False, True):
            with self.subTest(growth=growth):
                report = full_report(growth=growth)
                boundaries = dict(report["buy_zone"]["boundaries"])
                self.assertValid(report)
                self.assertEqual(report["buy_zone"]["boundaries"], boundaries)

    def test_all_four_links_are_required_not_a_generic_sentence(self):
        report = full_report()
        del report["buy_zone"]["normalization_evidence"]
        self.assertInvalid(report, "normalization_evidence")
        report["buy_zone"]["normalization_evidence"] = "More dividend evidence is needed."
        self.assertInvalid(report, "not of type 'object'")
        for link in ("operating_cash", "funding_capacity", "payout_policy", "entitled_shares"):
            with self.subTest(link=link):
                report = full_report()
                del report["buy_zone"]["normalization_evidence"][link]
                self.assertInvalid(report, link)

    def test_unknown_duplicate_category_alias_cannot_replace_a_link(self):
        report = full_report()
        report["buy_zone"]["normalization_evidence"]["operating_cash_again"] = (
            report["buy_zone"]["normalization_evidence"]["operating_cash"].copy()
        )
        self.assertInvalid(report, "Additional properties")

    def test_supported_and_conflicting_links_need_declared_sources(self):
        for status in ("supported", "conflicting"):
            with self.subTest(status=status):
                report = full_report()
                if status == "conflicting":
                    mark_operating_gap(report, status)
                row = report["buy_zone"]["normalization_evidence"]["operating_cash"]
                row["source_refs"] = []
                self.assertInvalid(report, "non-empty")
                row["source_refs"] = ["A source not declared in this report"]
                self.assertInvalid(report, "declared report sources")
                row["source_refs"] = [EVIDENCE]
                self.assertValid(report)

    def test_evidence_fields_cannot_be_blank_or_omitted(self):
        for field in ("input_detail", "consequence", "resolution_source"):
            for value in ("", " \n\t"):
                with self.subTest(field=field, value=value):
                    report = full_report()
                    mark_operating_gap(report)
                    report["buy_zone"]["normalization_evidence"]["operating_cash"][field] = value
                    self.assertInvalid(report, "does not match")
        report = full_report()
        del report["buy_zone"]["normalization_evidence"]["payout_policy"]["consequence"]
        self.assertInvalid(report, "consequence")

    def test_missing_requires_resolution_supported_does_not_invent_a_gap(self):
        report = full_report()
        mark_operating_gap(report)
        row = report["buy_zone"]["normalization_evidence"]["operating_cash"]
        row["resolution_source"] = None
        self.assertInvalid(report, "not of type 'string'")
        row.update(status="supported", source_refs=[EVIDENCE])
        self.assertValid(report)
        row["resolution_source"] = "Unresolved operating evidence"
        self.assertInvalid(report, "None was expected")

    def test_partial_evidence_preserves_supported_policy_and_shares(self):
        report = full_report()
        mark_operating_gap(report)
        report["buy_zone"]["normalized_net_dps_basis"] = "three_year_base_average"
        report["dividend_and_yield_runway"][1]["dps_source"] = "illustrative"
        self.assertValid(report)
        evidence = report["buy_zone"]["normalization_evidence"]
        self.assertEqual(evidence["payout_policy"]["status"], "supported")
        self.assertEqual(evidence["entitled_shares"]["status"], "supported")
        report["action_assessment"]["status"] = "eligible"
        self.assertInvalid(report, "Incomplete normalization evidence")

    def test_illustrative_average_cannot_claim_an_all_supported_checklist(self):
        report = full_report()
        report["buy_zone"]["normalized_net_dps_basis"] = "three_year_base_average"
        report["dividend_and_yield_runway"][1]["dps_source"] = "illustrative"
        report["action_assessment"]["status"] = "diagnostic_only"
        self.assertInvalid(report, "missing or conflicting evidence link")
        mark_operating_gap(report)
        self.assertValid(report)

    def test_incomplete_secondary_income_comparison_can_be_omitted(self):
        report = full_report(growth=True)
        mark_operating_gap(report)
        report["action_assessment"]["status"] = "eligible"
        self.assertInvalid(report, "Incomplete normalization evidence")
        report.pop("buy_zone")
        self.assertValid(report)

    def test_old_schema_version_requires_explicit_migration(self):
        report = full_report()
        for version in ("2.1", "2.2"):
            report["schema_version"] = version
            self.assertInvalid(report, "2.3")


if __name__ == "__main__":
    unittest.main()
