"""Cross-file contracts for the locally merged skill, not investment evidence."""

from pathlib import Path
import json
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
if (ROOT / "dividend-income-equity-analysis").is_dir():
    ROOT /= "dividend-income-equity-analysis"


class SkillInstallationTests(unittest.TestCase):
    def test_entry_file_references_exist(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        references = re.findall(r"`([^`\n]+\.(?:md|json|html|py|txt))`", text)
        self.assertTrue(references)
        for reference in references:
            if "<" not in reference:
                self.assertTrue((ROOT / reference).is_file(), reference)

    def test_no_unresolved_merge_markers(self):
        for path in ROOT.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".json", ".html", ".py"}:
                self.assertNotRegex(
                    path.read_text(encoding="utf-8"),
                    r"(?m)^(?:<{7}|={7}|>{7}|\|{7})(?: |$)",
                    str(path.relative_to(ROOT)),
                )

    def test_default_versions_and_preserved_modes(self):
        schema = json.loads((ROOT / "schema.json").read_text(encoding="utf-8"))
        version = schema["properties"]["schema_version"]
        self.assertEqual(version["default"], "3.0")
        self.assertEqual(version["enum"], ["2.3", "2.4", "2.5", "3.0"])
        self.assertEqual(
            set(schema["properties"]["mode"]["enum"]),
            {"screen", "full_analysis", "safety_review"},
        )

    def test_all_schema_references_resolve_locally(self):
        schema = json.loads((ROOT / "schema.json").read_text(encoding="utf-8"))

        def visit(node):
            if isinstance(node, dict):
                if "$ref" in node:
                    ref = node["$ref"]
                    self.assertTrue(ref.startswith("#/"), ref)
                    target = schema
                    for key in ref[2:].split("/"):
                        key = key.replace("~1", "/").replace("~0", "~")
                        target = target[int(key)] if isinstance(target, list) else target[key]
                for value in node.values():
                    visit(value)
            elif isinstance(node, list):
                for value in node:
                    visit(value)

        visit(schema)

    def test_current_rules_do_not_cancel_partial_scores(self):
        scoring = (ROOT / "scoring.md").read_text(encoding="utf-8")
        quality = (ROOT / "analysis-quality.md").read_text(encoding="utf-8")
        entry = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Recovery-First Scoring, Rubric 2", scoring)
        self.assertIn("scorecard.summary", quality)
        self.assertNotIn("If any component is unassessable, set status `not_assessed`", quality)
        self.assertNotIn("adding it only for a complete legacy", scoring)
        self.assertNotIn("Schema 仍为 2.4", entry)
        self.assertIn("canonical_repository", entry)
        for marker in ("分层买点", "暂定区间", "中性补分", "税务", "Safety Review"):
            self.assertIn(marker, entry)

    def test_runtime_scripts_are_self_contained(self):
        for name in ("decision_rules.py", "validate_analysis.py"):
            self.assertTrue((ROOT / "scripts" / name).is_file())
        self.assertTrue((ROOT / "requirements-dev.txt").is_file())
        for name in ("analysis-quality.md", "report-language.md", "safety-review.md",
                     "templates\\report.html", "examples\\safety-review.analysis.json"):
            self.assertTrue((ROOT / name).is_file(), name)


if __name__ == "__main__":
    unittest.main()
