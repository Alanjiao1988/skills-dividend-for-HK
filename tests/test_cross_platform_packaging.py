"""Real isolated installs, distribution integrity and static discovery contracts."""
import copy
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import skill_package as package  # noqa: E402

NAME = package.NAME
TOOL = ROOT / "scripts" / "skill_package.py"
RUNS = ROOT / "validation-runs"
BASELINES = {
    "cmport-0144": (10.814159799622688, 9.192035829679284, "growth_valuation"),
    "hsbc-0005": (19.260233918128655, 17.33421052631579, "capital_return_valuation"),
}


def call(*args, cwd=None, ok=True, env=None):
    result = subprocess.run([sys.executable, "-B", str(TOOL), *map(str, args)],
                            cwd=cwd, text=True, capture_output=True, env=env)
    if ok and result.returncode:
        raise AssertionError(f"command failed: {args}\n{result.stdout}\n{result.stderr}")
    if not ok and not result.returncode:
        raise AssertionError(f"command unexpectedly succeeded: {args}")
    return result


class CrossPlatformPackagingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        cls.dist = cls.root / "distributions"
        call("build", "--output", cls.dist)
        call("verify", "--output", cls.dist)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def setUp(self):
        self.work = tempfile.TemporaryDirectory(dir=self.root)
        self.addCleanup(self.work.cleanup)
        self.workpath = Path(self.work.name)

    def install(self, platform, archive=True):
        project = self.workpath / platform / "separate-project"
        project.mkdir(parents=True)
        src = (self.dist / f"{platform}.zip" if archive else self.dist / platform / NAME)
        call("install", "--platform", platform, "--project", project, "--package", src,
             cwd=self.workpath)
        target = project.joinpath(*package.PLATFORMS[platform], NAME)
        return project, target, src

    def test_yaml_standard_and_resource_references(self):
        for platform in package.PLATFORMS:
            folder = self.dist / platform / NAME
            lines = (folder / "SKILL.md").read_text(encoding="utf-8").split("---", 2)
            front = yaml.safe_load(lines[1])
            self.assertEqual(front["name"], folder.name)
            self.assertRegex(front["name"], r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
            self.assertLessEqual(len(front["name"]), 64)
            self.assertGreater(len(front["description"]), 0)
            self.assertLessEqual(len(front["description"]), 1024)
            self.assertTrue(set(front) <= {"name", "description", "license", "compatibility", "metadata", "allowed-tools"})
            self.assertEqual(front["metadata"]["schema_version"], "3.0")
            files, _ = package.read_package(folder, platform)
            package.validate_skill({k: v for k, v in files.items() if k != package.MANIFEST})

    def test_rejects_invalid_frontmatter_or_missing_reference(self):
        files = package.source_files()
        entry = files["SKILL.md"].decode("utf8")
        for edit in (
            entry.replace("name: dividend-income-equity-analysis", "name: Dividend--Broken", 1),
            entry.replace('description: "', 'description: "unclosed ', 1).replace('研究港股', '研究港股"broken', 1),
            entry.replace("`screen-mode.md`", "`missing-reference.md`", 1),
            entry.replace("name: dividend-income-equity-analysis", "name: dividend-income-equity-analysis\nname: duplicate", 1),
        ):
            changed = dict(files, **{"SKILL.md": edit.encode("utf8")})
            with self.assertRaises(package.PackageError):
                package.validate_skill(changed)

    def test_deterministic_build_and_detect_drift(self):
        before = {p: (self.dist / f"{p}.zip").read_bytes() for p in package.PLATFORMS}
        call("build", "--output", self.dist)
        self.assertEqual(before, {p: (self.dist / f"{p}.zip").read_bytes() for p in package.PLATFORMS})
        other = self.workpath / "copy"
        shutil.copytree(self.dist, other)
        (other / "codex" / NAME / "schema.json").write_text("{}", encoding="utf8")
        result = call("verify", "--output", other, ok=False)
        self.assertIn("modified", result.stderr)
        call("build", "--output", other, ok=False)
        self.assertEqual((other / "codex" / NAME / "schema.json").read_text(), "{}")

    def test_source_archive_does_not_borrow_parent_git_commit(self):
        if not shutil.which("git"):
            self.skipTest("Git required to construct the parent checkout")
        outer = self.workpath / "outer"
        outer.mkdir()
        subprocess.run(["git", "init", str(outer)], check=True, capture_output=True)
        archive_root = outer / "downloaded-source"
        (archive_root / "scripts").mkdir(parents=True)
        for name in ("skill_package.py", "skill-package-files.txt"):
            shutil.copyfile(ROOT / "scripts" / name, archive_root / "scripts" / name)
        shutil.copytree(ROOT / NAME, archive_root / NAME, ignore=shutil.ignore_patterns("__pycache__"))
        out = self.workpath / "archive-dist"
        subprocess.run([sys.executable, "-B", str(archive_root / "scripts/skill_package.py"),
                        "build", "--output", str(out)], check=True, capture_output=True)
        manifest = json.loads((out / "codex" / NAME / package.MANIFEST).read_text(encoding="utf8"))
        self.assertIsNone(manifest["source_commit"])
        self.assertEqual(manifest["source_status"], "unknown")

    def test_distribution_records_checkout_provenance(self):
        manifest = json.loads((self.dist / "codex" / NAME / package.MANIFEST).read_text(encoding="utf8"))
        source = package.provenance()
        self.assertEqual(manifest["source_commit"], source["commit"])
        self.assertEqual(manifest["source_status"], source["status"])

    def test_installs_at_documented_paths_and_is_idempotent(self):
        for platform in package.PLATFORMS:
            with self.subTest(platform=platform):
                project, target, src = self.install(platform)
                self.assertTrue((target / "SKILL.md").is_file())
                call("install", "--platform", platform, "--project", project, "--package", src)
                call("check", "--platform", platform, "--project", project, "--against", src)
                # A host starting from a child can search for this root; this is only a filesystem check.
                child = project / "packages" / "app"
                child.mkdir(parents=True)
                self.assertIn(project, child.parents)
                self.assertTrue(project.joinpath(*package.PLATFORMS[platform], NAME, "SKILL.md").is_file())

    def test_update_refuses_unmanaged_or_locally_modified_content(self):
        platform = "codex"
        project = self.workpath / "project"
        project.mkdir()
        target = project.joinpath(*package.PLATFORMS[platform], NAME)
        target.mkdir(parents=True)
        custom = target / "custom.txt"
        custom.write_text("user content", encoding="utf8")
        src = self.dist / "codex.zip"
        call("install", "--platform", platform, "--project", project, "--package", src, "--update", ok=False)
        self.assertEqual(custom.read_text(encoding="utf8"), "user content")
        shutil.rmtree(target)
        call("install", "--platform", platform, "--project", project, "--package", src)
        # An intact but different managed package needs explicit --update.
        manifest_path = target / package.MANIFEST
        manifest = json.loads(manifest_path.read_text(encoding="utf8"))
        manifest["source_commit"] = "0" * 40
        manifest_path.write_text(json.dumps(manifest), encoding="utf8")
        call("install", "--platform", platform, "--project", project, "--package", src, ok=False)
        call("install", "--platform", platform, "--project", project, "--package", src, "--update")
        skill = target / "SKILL.md"
        skill.write_text(skill.read_text(encoding="utf8") + "\nUser customization\n", encoding="utf8")
        result = call("install", "--platform", platform, "--project", project, "--package", src, "--update", ok=False)
        self.assertIn("modified", result.stderr)
        self.assertTrue(skill.read_text(encoding="utf8").endswith("User customization\n"))

    def test_personal_install_paths_are_separate_from_project_paths(self):
        fake_home = self.workpath / "home"
        fake_home.mkdir()
        env = os.environ.copy()
        env.update({"HOME": str(fake_home), "USERPROFILE": str(fake_home)})
        for platform, components in package.USER_PLATFORMS.items():
            src = self.dist / f"{platform}.zip"
            call("install", "--platform", platform, "--user", "--package", src, env=env)
            self.assertTrue(fake_home.joinpath(*components, NAME, "SKILL.md").is_file())
            call("check", "--platform", platform, "--user", "--against", src, env=env)

    def test_failed_upgrade_restores_previous_installation(self):
        project, target, src = self.install("codex")
        manifest_path = target / package.MANIFEST
        old = json.loads(manifest_path.read_text(encoding="utf8"))
        old["source_commit"] = "0" * 40
        manifest_path.write_text(json.dumps(old), encoding="utf8")
        original_rename = Path.rename

        def fail_new_move(path, destination):
            if path.name == NAME and path.parent.name.startswith(".skill-install-"):
                raise OSError("simulated failed install")
            return original_rename(path, destination)

        args = type("Args", (), {"package": src, "platform": "codex", "project": project,
                                  "user": False, "update": True})()
        with mock.patch.object(Path, "rename", fail_new_move):
            with self.assertRaisesRegex(OSError, "simulated failed install"):
                package.install(args)
        self.assertEqual(json.loads(manifest_path.read_text(encoding="utf8"))["source_commit"], "0" * 40)
        package.read_package(target, "codex")

    def test_empty_custom_directory_is_not_deleted_on_update(self):
        project, target, src = self.install("claude")
        custom = target / "my-empty-directory"
        custom.mkdir()
        call("install", "--platform", "claude", "--project", project,
             "--package", src, "--update", ok=False)
        self.assertTrue(custom.is_dir())

    def test_missing_runtime_dependency_has_install_hint(self):
        _, target, _ = self.install("codex")
        result = subprocess.run([sys.executable, "-S", str(target / "scripts/validate_analysis.py"),
                                 str(target / "examples/ordinary.analysis.json")],
                                cwd=self.workpath, text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing jsonschema", result.stderr)
        self.assertIn("pip install -r", result.stderr)

    def test_rejects_zip_slip_and_wrong_platform(self):
        evil = self.workpath / "evil.zip"
        with zipfile.ZipFile(evil, "w") as archive:
            archive.writestr(f"{NAME}/../../escape", "bad")
        call("install", "--platform", "codex", "--project", self.workpath, "--package", evil, ok=False)
        self.assertFalse((self.workpath / "escape").exists())
        call("install", "--platform", "claude", "--project", self.workpath,
             "--package", self.dist / "codex.zip", ok=False)

    def test_installed_examples_and_real_company_reports_from_unrelated_cwd(self):
        for platform in package.PLATFORMS:
            with self.subTest(platform=platform):
                _, target, src = self.install(platform)
                # This subprocess cannot import from the checkout through the working directory.
                probe = ("import json,sys; from pathlib import Path; "
                         "p=Path(sys.argv[1]); sys.path.insert(0,str(p)); "
                         "import scripts.validate_analysis, scripts.render_report, scripts.decision_rules; "
                         "assert scripts.validate_analysis.ROOT == p; "
                         "s=json.loads((p/'schema.json').read_text(encoding='utf8')); "
                         "assert s['properties']['schema_version']['default']=='3.0'; "
                         "assert (p/'templates/report.html').is_file()")
                subprocess.run([sys.executable, "-B", "-c", probe, str(target)], cwd=self.workpath,
                               check=True, capture_output=True)
                for example in ("ordinary", "growth", "safety-review", "full-report"):
                    subprocess.run([sys.executable, "-B", str(target / "scripts/validate_analysis.py"),
                                    str(target / f"examples/{example}.analysis.json")],
                                   cwd=self.workpath, check=True, capture_output=True)
                for name, (valuation, starter, valuation_key) in BASELINES.items():
                    original = next(RUNS.glob(f"*/{name}.analysis.json"))
                    data = json.loads(original.read_text(encoding="utf8"))
                    external = self.workpath / f"{platform}-{name}.json"
                    shutil.copyfile(original, external)
                    out = self.workpath / f"{platform}-{name}.html"
                    for script, paths in (("validate_analysis.py", [external]),
                                          ("render_report.py", [external, out])):
                        subprocess.run([sys.executable, "-B", str(target / "scripts" / script),
                                        *map(str, paths)], cwd=self.workpath, check=True, capture_output=True)
                    rendered = out.read_text(encoding="utf8")
                    self.assertEqual(rendered, original.with_name(f"{name}.html").read_text(encoding="utf8"))
                    self.assertEqual(len(re.findall(r'<section id="section-\d+">', rendered)), 12)
                    for number in range(1, 14):
                        self.assertRegex(rendered, rf">A{number} [^<]+</h3>")
                    self.assertAlmostEqual(data[valuation_key]["base_case_value"], valuation)
                    self.assertAlmostEqual(data["decision"]["reference_prices"]["starter"], starter)
                call("check", "--platform", platform, "--project", target.parents[2], "--against", src)

    def test_static_discovery_scenarios_are_described_not_runtime_claims(self):
        front = yaml.safe_load((package.SOURCE / "SKILL.md").read_text(encoding="utf8").split("---", 2)[1])
        description = front["description"]
        # Case 1 explicit invocation; case 2 stock Full Analysis; case 3 unrelated request.
        self.assertEqual(front["name"], "dividend-income-equity-analysis")
        for token in ("股息安全", "估值", "买入价格", "Full Analysis", "十二章", "dividend sustainability"):
            self.assertIn(token, description)
        for exclusion in ("无关编程", "普通文档", "金融术语"):
            self.assertIn(exclusion, description)
        self.assertNotIn("disable-model-invocation", front)
        self.assertNotIn("user-invocable", front)
        # These checks cannot prove an LLM will select a skill for a given prompt.

    def test_full_analysis_instructions_are_loaded_by_mode(self):
        entry = (package.SOURCE / "SKILL.md").read_text(encoding="utf8")
        full = (package.SOURCE / "full-analysis.md").read_text(encoding="utf8")
        self.assertIn("每次 Full Analysis 必须完整读取 `full-analysis.md`", entry)
        self.assertIn("Screen Mode 必须读取 `screen-mode.md`", entry)
        for marker in ("Bear / Base / Bull", "每项Capex", "先运行红利陷阱", "每项评分", "最终结论必须区分"):
            self.assertIn(marker, full)
        self.assertNotIn("每项Capex", entry)


if __name__ == "__main__":
    unittest.main()
