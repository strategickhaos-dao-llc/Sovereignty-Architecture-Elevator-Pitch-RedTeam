"""
Unit tests for the example_ingot.
"""
import sys
from pathlib import Path

# Add parent directories to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from ingots.example_ingot.src.main import process


class TestExampleIngot:
    """Test cases for example_ingot process function."""

    def test_process_string_input(self):
        """Test processing a string input."""
        result = process("Strategickhaos Baby")
        assert result["input"] == "Strategickhaos Baby"
        assert result["length"] == 19
        assert result["is_numeric"] is False

    def test_process_numeric_string(self):
        """Test processing a numeric string."""
        result = process("12345")
        assert result["input"] == "12345"
        assert result["length"] == 5
        assert result["is_numeric"] is True

    def test_process_integer_input(self):
        """Test processing an integer input."""
        result = process(12345)
        assert result["input"] == 12345
        assert result["length"] == 5
        assert result["is_numeric"] is True

    def test_process_empty_string(self):
        """Test processing an empty string."""
        result = process("")
        assert result["input"] == ""
        assert result["length"] == 0
        assert result["is_numeric"] is False

    def test_process_mixed_content(self):
        """Test processing mixed alphanumeric content."""
        result = process("abc123")
        assert result["input"] == "abc123"
        assert result["length"] == 6
        assert result["is_numeric"] is False

    def test_process_float_input(self):
        """Test processing a float input."""
        result = process(3.14)
        assert result["input"] == 3.14
        assert result["length"] == 4
        assert result["is_numeric"] is False  # Contains decimal point

    def test_process_special_characters(self):
        """Test processing special characters."""
        result = process("!@#$%")
        assert result["input"] == "!@#$%"
        assert result["length"] == 5
        assert result["is_numeric"] is False


def run_tests():
    """Run all tests and report results."""
    test_instance = TestExampleIngot()
    tests = [
        method
        for method in dir(test_instance)
        if method.startswith("test_")
    ]

    passed = 0
    failed = 0

    for test_name in tests:
        try:
            getattr(test_instance, test_name)()
            print(f"✅ {test_name}")
            passed += 1
        except AssertionError as e:
            print(f"❌ {test_name}: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test_name}: {type(e).__name__}: {e}")
            failed += 1

    print(f"\n{'='*40}")
    print(f"Tests: {passed + failed}, Passed: {passed}, Failed: {failed}")
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
