"""Verify independent worked answers and reproducible source attribution."""
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.validate_analysis import validate_report

ROOT = Path(__file__).resolve().parents[1]


class WorkedExampleTests(unittest.TestCase):
    def load(self, mode):
        return json.loads((ROOT / f'dividend-income-equity-analysis/examples/{mode}.analysis.json').read_text(encoding='utf8'))

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

    def test_fixture_dividend_cannot_be_edited_without_funding_reconciliation(self):
        report = self.load('ordinary')
        report['dividend_and_yield_runway'][0]['derived_dps'] += 1
        self.assertTrue(validate_report(report))


class BundleProvenanceTests(unittest.TestCase):
    def setUp(self):
        candidate = Path('C:/Program Files/Git/bin/bash.exe')
        self.bash = str(candidate) if os.name == 'nt' and candidate.is_file() else shutil.which('bash')
        if not self.bash or not shutil.which('git'):
            self.skipTest('Bundle provenance needs Git and Bash')
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def copy_sources(self, destination):
        destination.mkdir(parents=True, exist_ok=True)
        for name in ('build-gpt-instructions.sh', 'gpt-header.md'):
            shutil.copyfile(ROOT / name, destination / name)
        shutil.copytree(ROOT / 'dividend-income-equity-analysis', destination / 'dividend-income-equity-analysis')

    def git(self, cwd, *args):
        return subprocess.check_output(['git', '-C', str(cwd), *args], stderr=subprocess.DEVNULL).decode().strip()

    def build(self, cwd, mode='all'):
        subprocess.run([self.bash, 'build-gpt-instructions.sh', '--mode', mode], cwd=cwd, check=True, capture_output=True)
        name = 'chatgpt-custom-gpt-instructions.md' if mode == 'all' else 'chatgpt-screen-instructions.md'
        return (cwd / 'dist' / name).read_text(encoding='utf8')

    def test_source_archive_does_not_borrow_enclosing_repo_identity(self):
        self.git(self.root, 'init')
        child = self.root / 'source-archive'
        self.copy_sources(child)
        text = self.build(child)
        self.assertIn('Source commit: `unknown`', text)
        self.assertIn('Schema version: `3.0`', text)
        self.assertEqual(text, self.build(child))

    def test_clean_commit_then_relevant_untracked_source_is_dirty(self):
        self.copy_sources(self.root)
        self.git(self.root, 'init')
        (self.root / '.gitignore').write_text('dist/\n', encoding='utf8')
        self.git(self.root, 'add', '.')
        self.git(self.root, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-m', 'Fixture sources')
        sha = self.git(self.root, 'rev-parse', 'HEAD')
        text = self.build(self.root)
        self.assertIn(f'Source commit: `{sha}`', text)
        self.assertIn('Source status: `clean`', text)
        (self.root / 'dividend-income-equity-analysis/new-source.md').write_text('Uncommitted source', encoding='utf8')
        self.assertIn('Source status: `dirty`', self.build(self.root))

    def test_screen_keeps_provenance_and_portfolio_context_without_valuation_modules(self):
        self.copy_sources(self.root)
        text = self.build(self.root, mode='screen')
        self.assertIn('Bundle profile: `screen`', text)
        self.assertIn('Source commit: `unknown`', text)
        self.assertIn('Build-input SHA-256:', text)
        modules = [line for line in text.splitlines() if line.startswith('# Module: ')]
        self.assertEqual(modules, [f'# Module: {name}' for name in (
            'data-conventions.md', 'portfolio-context.md', 'screen-mode.md', 'withholding-notes.md',
            'report-language.md')])
        self.assertEqual(text, self.build(self.root, mode='screen'))

    def test_invalid_profile_does_not_overwrite_a_bundle(self):
        self.copy_sources(self.root)
        before = self.build(self.root)
        result = subprocess.run([self.bash, 'build-gpt-instructions.sh', '--mode', 'invalid'],
                                cwd=self.root, capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(before, (self.root / 'dist/chatgpt-custom-gpt-instructions.md').read_text(encoding='utf8'))
