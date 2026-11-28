import unittest
from report import generate_report, summarize

RECS = [{"category": "food", "amount": 10}, {"category": "food", "amount": 20},
        {"category": "gear", "amount": 30.5}]

class TestReport(unittest.TestCase):
    def test_summarize(self):
        s = summarize(RECS)
        self.assertEqual(s["total"], 60.5)
        self.assertEqual(s["count"], 3)
        self.assertEqual(s["average"], 20.17)
        self.assertEqual(s["by_category"], {"food": 30.0, "gear": 30.5})
    def test_summarize_empty(self):
        self.assertEqual(summarize([]), {"total": 0.0, "count": 0, "average": 0.0, "by_category": {}})
    def test_text_report(self):
        out = generate_report(RECS, "text")
        self.assertIn("REPORT", out)
        self.assertIn("TOTAL", out)
        self.assertIn("60.50", out)
        self.assertIn("AVERAGE", out)
        self.assertIn("20.17", out)
    def test_csv_report(self):
        out = generate_report(RECS, "csv")
        lines = out.splitlines()
        self.assertEqual(lines[0], "category,amount")
        self.assertEqual(lines[1], "food,10.00")
        self.assertEqual(len(lines), 4)
    def test_bad_format(self):
        with self.assertRaises(ValueError):
            generate_report(RECS, "xml")
    def test_validation(self):
        for bad in ([{"amount": 1}], [{"category": "x"}], [{"category": "x", "amount": -1}],
                    [{"category": "x", "amount": "no"}], ["nope"]):
            with self.assertRaises(ValueError):
                summarize(bad)
            with self.assertRaises(ValueError):
                generate_report(bad, "text")

if __name__ == "__main__":
    unittest.main()
