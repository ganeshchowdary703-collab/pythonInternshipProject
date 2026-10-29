"""Automated tests:  python test_portfolio_tracker.py"""
import csv
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import portfolio_tracker as pt


def run_main(inputs):
    out = io.StringIO()
    with patch("builtins.input", side_effect=inputs), redirect_stdout(out):
        pt.main()
    return out.getvalue()


class TestCalculation(unittest.TestCase):
    def test_total(self):
        rows, total = pt.calculate({"AAPL": 10, "TSLA": 5})
        self.assertEqual(total, 10 * 180 + 5 * 250)
        self.assertEqual(rows[0], ("AAPL", 10, 180, 1800))

    def test_empty_portfolio(self):
        self.assertEqual(pt.calculate({}), ([], 0))

    def test_custom_prices(self):
        self.assertEqual(pt.calculate({"X": 3}, {"X": 2.5})[1], 7.5)

    def test_money_format(self):
        self.assertEqual(pt.money(1234.5), "$1,234.50")


class TestInput(unittest.TestCase):
    def test_symbol_is_case_insensitive_and_retries(self):
        with patch("builtins.input", side_effect=["xyz", "", "aapl"]), redirect_stdout(io.StringIO()):
            self.assertEqual(pt.ask_symbol(), "AAPL")

    def test_done_returns_none(self):
        with patch("builtins.input", side_effect=["Done"]):
            self.assertIsNone(pt.ask_symbol())

    def test_quantity_validation(self):
        with patch("builtins.input", side_effect=["abc", "-3", "2.5", "0", "7"]), redirect_stdout(io.StringIO()):
            self.assertEqual(pt.ask_quantity("AAPL"), 7)

    def test_same_stock_twice_is_combined(self):
        inputs = ["AAPL", "3", "aapl", "4", "done"]
        with patch("builtins.input", side_effect=inputs), redirect_stdout(io.StringIO()):
            self.assertEqual(pt.collect_portfolio(), {"AAPL": 7})


class TestFiles(unittest.TestCase):
    def setUp(self):
        self.rows, self.total = pt.calculate({"AAPL": 10, "TSLA": 5})
        self.dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.dir.cleanup()

    def test_save_txt(self):
        path = os.path.join(self.dir.name, "p.txt")
        pt.save_txt(self.rows, self.total, path)
        text = open(path, encoding="utf-8").read()
        self.assertIn("TOTAL INVESTMENT", text)
        self.assertIn("$3,050.00", text)

    def test_save_csv(self):
        path = os.path.join(self.dir.name, "p.csv")
        pt.save_csv(self.rows, self.total, path)
        data = list(csv.reader(open(path, encoding="utf-8")))
        self.assertEqual(data[0], ["Stock", "Shares", "Price", "Value"])
        self.assertEqual(data[1], ["AAPL", "10", "180", "1800"])
        self.assertEqual(data[-1], ["TOTAL", "", "", "3050"])


class TestFullProgram(unittest.TestCase):
    def test_end_to_end_and_save(self):
        with tempfile.TemporaryDirectory() as d:
            cwd = os.getcwd(); os.chdir(d)
            try:
                out = run_main(["AAPL", "10", "TSLA", "5", "done", "csv"])
                self.assertIn("$3,050.00", out)
                self.assertTrue(os.path.exists("portfolio.csv"))
            finally:
                os.chdir(cwd)

    def test_no_stocks_entered(self):
        self.assertIn("No stocks entered", run_main(["done"]))

    def test_declining_to_save_creates_no_file(self):
        with tempfile.TemporaryDirectory() as d:
            cwd = os.getcwd(); os.chdir(d)
            try:
                run_main(["MSFT", "1", "done", "no"])
                self.assertEqual(os.listdir("."), [])
            finally:
                os.chdir(cwd)


if __name__ == "__main__":
    unittest.main(verbosity=2)
