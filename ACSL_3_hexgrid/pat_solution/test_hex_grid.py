import os
import unittest
import tempfile
import shutil

import hex_grid


class TestParser(unittest.TestCase):
    def test_simple(self):
        instruction = "B33 12345"
        parsed = hex_grid.parse_input_line(instruction)
        self.assertEqual(parsed.row, "33")
        self.assertEqual(parsed.col, "B")
        self.assertEqual(parsed.moves, "12345")


class TestIndividualCells(unittest.TestCase):
    def test_even_row_mid(self):
        test_data = (
            ("B3", 1, "up", "B4", "Even row, middle of grid"),
            ("B3", 2, "Ur", "C3", "Even row, middle of grid"),
            ("B3", 3, "Dr", "C2", "Even row, middle of grid"),
            ("B3", 4, "dn", "B2", "Even row, middle of grid"),
            ("B3", 5, "Dl", "A2", "Even row, middle of grid"),
            ("B3", 6, "Ul", "A3", "Even row, middle of grid"),

            ("C4", 1, "up", "C5", "Odd row, middle of grid"),
            ("C4", 2, "Ur", "D5", "Odd row, middle of grid"),
            ("C4", 3, "Dr", "D4", "Odd row, middle of grid"),
            ("C4", 4, "dn", "C3", "Odd row, middle of grid"),
            ("C4", 5, "Dl", "B4", "Odd row, middle of grid"),
            ("C4", 6, "Ul", "B5", "Odd row, middle of grid"),

            ("A3", 1, "up", "A4", "Left edge, middle of col"),
            ("A3", 2, "Ur", "B4", "Left edge, middle of col"),
            ("A3", 3, "Dr", "B3", "Left edge, middle of col"),
            ("A3", 4, "dn", "A2", "Left edge, middle of col"),
            ("A3", 5, "Dl", "A3", "Left edge, middle of col"),
            ("A3", 6, "Ul", "A3", "Left edge, middle of col"),

            ("A1", 1, "up", "A2", "Bottom left corner"),
            ("A1", 2, "Ur", "B2", "Bottom left corner"),
            ("A1", 3, "Dr", "B1", "Bottom left corner"),
            ("A1", 4, "dn", "A1", "Bottom left corner"),
            ("A1", 5, "Dl", "A1", "Bottom left corner"),
            ("A1", 6, "Ul", "A1", "Bottom left corner"),

            ("B1", 1, "up", "B2", "Bottom row middle of row"),
            ("B1", 2, "Ur", "C1", "Bottom row middle of row"),
            ("B1", 3, "Dr", "B1", "Bottom row middle of row"),
            ("B1", 4, "dn", "B1", "Bottom row middle of row"),
            ("B1", 5, "Dl", "B1", "Bottom row middle of row"),
            ("B1", 6, "Ul", "A1", "Even row, middle of grid"),

            # For sanity, LAST_COL assumed to be Z
            ("Z3", 1, "up", "Z4", "Last col, middle of col"),
            ("Z3", 2, "Ur", "Z3", "Last col, middle of col"),
            ("Z3", 3, "Dr", "Z3", "Last col, middle of col"),
            ("Z3", 4, "dn", "Z2", "Last col, middle of col"),
            ("Z3", 5, "Dl", "Y2", "Last col, middle of col"),
            ("Z3", 6, "Ul", "Y3", "Last col, middle of col"),

            ("Z1", 1, "up", "Z2", "Bottom right corner"),
            ("Z1", 2, "Ur", "Z1", "Bottom right corner"),
            ("Z1", 3, "Dr", "Z1", "Bottom right corner"),
            ("Z1", 4, "dn", "Z1", "Bottom right corner"),
            ("Z1", 5, "Dl", "Z1", "Bottom right corner"),
            ("Z1", 6, "Ul", "Y1", "Bottom right corner"),
        )

        for beg, move, label, target, location in test_data:
            parsed = hex_grid.parse_input_line(f"{beg} {move}")
            chr_to_col, col_to_chr = hex_grid.fetch_chr_to_ord_dicts()
            result = hex_grid.process_data(parsed, chr_to_col, col_to_chr)
            msg = f"{location}:{beg} move:{move}({label}) target: {target} result: {result}"
            self.assertEqual(result, target, msg)


# @unittest.skip("test atomic first")
class TestFiles(unittest.TestCase):
    SAMPLE_INPUT_PATH = "sample_input.txt"
    SAMPLE_TARGET_OUTPUT_PATH = "sample_output.txt"
    SAMPLE_RESULTS_PATH = "sample_results.txt"
    TEST_INPUT_PATH = "test_input.txt"
    TEST_TARGET_OUTPUT_PATH = "test_output.txt"
    TEST_RESULTS_PATH = "test_results.txt"

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_sampledata(self):
        hex_grid.main(
            self.SAMPLE_INPUT_PATH, os.path.join(self.tempdir, self.SAMPLE_RESULTS_PATH)
        )
        target = open(self.SAMPLE_TARGET_OUTPUT_PATH, "r")
        actual = open(os.path.join(self.tempdir, self.SAMPLE_RESULTS_PATH), "r")
        for trgt, actl in zip(target, actual):
            self.assertEqual(
                trgt, actl, f"sample data issue - target: {trgt}   actual: {actl}"
            )
        target.close()
        actual.close()

    def test_testdata(self):
        hex_grid.main(
            self.TEST_INPUT_PATH, os.path.join(self.tempdir, self.TEST_RESULTS_PATH)
        )
        target = open(self.TEST_TARGET_OUTPUT_PATH, "r")
        actual = open(os.path.join(self.tempdir, self.TEST_RESULTS_PATH), "r")
        for trgt, actl in zip(target, actual):
            self.assertEqual(
                trgt, actl, f"test data issue target: {trgt}   actual: {actl}"
            )
        target.close()
        actual.close()


if __name__ == "__main__":
    unittest.main()