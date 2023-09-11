import unittest
from pesel_utils import rotate_identifier, date_to_letters, format_pesel

class TestPeselUtils(unittest.TestCase):
    def test_rotate_identifier(self):
        # Test cases for the rotate_identifier function
        self.assertEqual(rotate_identifier("12345678901"), "89012345604")
        self.assertEqual(rotate_identifier("00000000000"), "77777777777")
        # Add more test cases as needed

    def test_date_to_letters(self):
        # Test cases for the date_to_letters function
        self.assertEqual(date_to_letters(), "ABCDEFGHII")
        # Add more test cases as needed

    def test_format_pesel(self):
        # Test cases for the format_pesel function
        self.assertEqual(format_pesel("89012345604"), "AB 8C DEFGH I IJ 0K LMNO 4P QRS 7TU VWXY 9Z 01")
        # Add more test cases as needed

if __name__ == '__main__':
    unittest.main()
