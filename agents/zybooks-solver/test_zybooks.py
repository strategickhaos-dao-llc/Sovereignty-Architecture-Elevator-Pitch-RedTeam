#!/usr/bin/env python3
"""
Test suite for zyBooks Solver Agent
"""

import sys
from pathlib import Path

# Add the agent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from parser import ZyBooksParser
from solver import ZyBooksSolver
from responder import ZyBooksResponder


def test_parser():
    """Test the parser module"""
    print("🧪 Testing Parser...")
    
    sample_content = """
    Section 1.5 - Participation Activity
    
    1) True or False: The mean is always greater than the median.
    True
    False
    
    2) What percentage of data falls within one standard deviation?
    a) 50%
    b) 68%
    c) 95%
    d) 99%
    
    3) In a normal distribution, approximately 95% of data falls within how many standard deviations?
    a) 1
    b) 2
    c) 3
    d) 4
    """
    
    parser = ZyBooksParser()
    
    # Test detection
    assert parser.is_zybooks_content(sample_content), "Failed to detect zyBooks content"
    print("  ✅ Detection works")
    
    # Test parsing
    result = parser.parse(sample_content)
    assert result["detected"] == True, "Detection flag not set"
    assert result["section"] == "1.5", f"Wrong section: {result['section']}"
    assert result["question_count"] == 3, f"Wrong question count: {result['question_count']}"
    print(f"  ✅ Parsed {result['question_count']} questions from section {result['section']}")
    
    # Test question types
    questions = result["questions"]
    assert questions[0]["type"] == "true_false", f"Wrong type for Q1: {questions[0]['type']}"
    assert questions[1]["type"] in ["multiple_choice", "numeric"], f"Wrong type for Q2: {questions[1]['type']}"
    print("  ✅ Question type detection works")
    
    return result


def test_solver(parsed_result):
    """Test the solver module"""
    print("\n🧪 Testing Solver...")
    
    questions = parsed_result["questions"]
    
    solver = ZyBooksSolver()
    answers = solver.solve(questions)
    
    assert len(answers) == len(questions), "Answer count mismatch"
    print(f"  ✅ Generated {len(answers)} answers")
    
    # Check answer structure
    for answer in answers:
        assert hasattr(answer, 'question_id'), "Missing question_id"
        assert hasattr(answer, 'answer'), "Missing answer"
        assert hasattr(answer, 'confidence'), "Missing confidence"
        assert hasattr(answer, 'reasoning'), "Missing reasoning"
        assert 0 <= answer.confidence <= 1, f"Invalid confidence: {answer.confidence}"
    print("  ✅ All answers have required fields")
    
    # Check specific answers
    q1_answer = next(a for a in answers if a.question_id == "q1")
    assert q1_answer.answer == "FALSE", f"Wrong answer for Q1: {q1_answer.answer}"
    assert q1_answer.confidence >= 0.7, f"Low confidence for Q1: {q1_answer.confidence}"
    print(f"  ✅ Q1: {q1_answer.answer} (confidence: {q1_answer.confidence:.2f})")
    
    return solver.get_answers()


def test_responder(section, answers):
    """Test the responder module"""
    print("\n🧪 Testing Responder...")
    
    responder = ZyBooksResponder()
    
    # Test YAML format
    yaml_output = responder.respond(section, answers, "yaml")
    assert "section:" in yaml_output, "YAML missing section"
    assert "answers:" in yaml_output, "YAML missing answers"
    print("  ✅ YAML format works")
    
    # Test rapid fire format
    rapid_output = responder.respond(section, answers, "rapid")
    assert "🔥 ANSWERS" in rapid_output, "Rapid format missing header"
    assert "q1:" in rapid_output, "Rapid format missing questions"
    print("  ✅ Rapid fire format works")
    
    # Test table format
    table_output = responder.respond(section, answers, "table")
    assert "┌" in table_output, "Table format missing borders"
    assert "Q#" in table_output, "Table format missing headers"
    print("  ✅ Table format works")
    
    # Test vessel mode
    vessel_output = responder.vessel_response(section, answers)
    assert f"Section {section}" in vessel_output, "Vessel mode missing section"
    print("  ✅ VESSEL mode works")
    
    return yaml_output


def test_flamelang_compression():
    """Test FlameLang semantic compression"""
    print("\n🧪 Testing FlameLang Compression...")
    
    solver = ZyBooksSolver()
    
    # Test compression
    text = "The mean is always greater than the median in normal distributions"
    compressed = solver.flamelang_compress(text)
    
    assert "english" in compressed, "Missing english layer"
    assert "hebrew" in compressed, "Missing hebrew layer"
    assert "wave" in compressed, "Missing wave layer"
    assert "dna" in compressed, "Missing dna layer"
    
    print(f"  ✅ English: {compressed['english']}")
    print(f"  ✅ Hebrew: {compressed['hebrew']}")
    print(f"  ✅ Wave: {compressed['wave']}")
    print(f"  ✅ DNA: {compressed['dna']}")
    
    return compressed


def test_edge_cases():
    """Test edge cases and error handling"""
    print("\n🧪 Testing Edge Cases...")
    
    parser = ZyBooksParser()
    
    # Test non-zyBooks content
    non_zybooks = "This is just random text without any zyBooks patterns"
    result = parser.parse(non_zybooks)
    assert result["detected"] == False, "False positive detection"
    print("  ✅ Correctly rejects non-zyBooks content")
    
    # Test empty content
    empty_result = parser.parse("")
    assert empty_result["detected"] == False, "Empty content detected as zyBooks"
    print("  ✅ Handles empty content")
    
    # Test with minimal markers
    minimal = "Section 1.2\n\n1) True\nFalse"
    minimal_result = parser.parse(minimal)
    # Should still work with minimal content
    print("  ✅ Handles minimal content")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🔥 zyBooks Solver Agent - Test Suite")
    print("=" * 60)
    
    try:
        # Test parser
        parsed_result = test_parser()
        
        # Test solver
        answers = test_solver(parsed_result)
        
        # Test responder
        yaml_output = test_responder(parsed_result["section"], answers)
        
        # Test FlameLang
        test_flamelang_compression()
        
        # Test edge cases
        test_edge_cases()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)
        print("\n📋 Sample Output (YAML):")
        print(yaml_output)
        
        return True
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
