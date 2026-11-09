"""Table numbers: amounts keep thousands separators; only year columns print bare four-digit years."""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "dividend-income-equity-analysis"))

from scripts.render_report import is_year_column, render_table  # noqa: E402


def cells(html_text):
    return re.findall(r"<td[^>]*>(.*?)</td>", html_text)


class TableNumberFormatTests(unittest.TestCase):
    def test_amount_in_year_range_keeps_separator_and_fiscal_year_does_not(self):
        html_text = render_table({
            "title": "五年经营与股东回报",
            "columns": ["财年", "联营合营现金分红", "到期年"],
            "rows": [[2025, 2034, 2040], ["2023", 2034, None]],
            "note": "百万港元"})
        self.assertEqual(cells(html_text), ["2025", "2,034", "2040", "2023", "2,034", "—"])
        self.assertNotIn(">2034<", html_text)

    def test_year_words_inside_amount_headers_do_not_mark_a_year_column(self):
        for header in ("财年", "到期年", "年份", "Fiscal year", "FY", "财年（截至 12 月）"):
            with self.subTest(header=header):
                self.assertTrue(is_year_column(header))
        for header in ("五年股息现值", "三年累计股息", "美国 10 年期国债", "当年派息", "五年", "FY+1", "收入"):
            with self.subTest(header=header):
                self.assertFalse(is_year_column(header))

    def test_amount_column_with_year_word_keeps_separator(self):
        html_text = render_table({"title": "t", "columns": ["情景", "五年股息现值"],
                                  "rows": [["Base", 2100]], "note": "n"})
        self.assertIn("2,100", html_text)


if __name__ == "__main__":
    unittest.main()
