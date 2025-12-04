"""
Unit tests for the example_ingot.
"""
import unittest

from ingots.example_ingot.src.main import process


class TestExampleIngot(unittest.TestCase):
    """Test cases for example_ingot process function."""

    def test_process_string_input(self):
        """Test processing a string input."""
        result = process("Strategickhaos Baby")
        self.assertEqual(result["input"], "Strategickhaos Baby")
        self.assertEqual(result["length"], 19)
        self.assertFalse(result["is_numeric"])

    def test_process_numeric_string(self):
        """Test processing a numeric string."""
        result = process("12345")
        self.assertEqual(result["input"], "12345")
        self.assertEqual(result["length"], 5)
        self.assertTrue(result["is_numeric"])

    def test_process_integer_input(self):
        """Test processing an integer input."""
        result = process(12345)
        self.assertEqual(result["input"], 12345)
        self.assertEqual(result["length"], 5)
        self.assertTrue(result["is_numeric"])

    def test_process_empty_string(self):
        """Test processing an empty string."""
        result = process("")
        self.assertEqual(result["input"], "")
        self.assertEqual(result["length"], 0)
        self.assertFalse(result["is_numeric"])

    def test_process_mixed_content(self):
        """Test processing mixed alphanumeric content."""
        result = process("abc123")
        self.assertEqual(result["input"], "abc123")
        self.assertEqual(result["length"], 6)
        self.assertFalse(result["is_numeric"])

    def test_process_float_input(self):
        """Test processing a float input."""
        result = process(3.14)
        self.assertEqual(result["input"], 3.14)
        self.assertEqual(result["length"], 4)
        self.assertFalse(result["is_numeric"])  # Contains decimal point

    def test_process_special_characters(self):
        """Test processing special characters."""
        result = process("!@#$%")
        self.assertEqual(result["input"], "!@#$%")
        self.assertEqual(result["length"], 5)
        self.assertFalse(result["is_numeric"])


if __name__ == "__main__":
    unittest.main()
