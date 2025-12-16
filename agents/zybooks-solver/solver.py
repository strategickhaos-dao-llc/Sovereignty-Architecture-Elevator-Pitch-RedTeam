"""
zyBooks Question Solver
Purpose: Apply FlameLang logic and statistical reasoning to solve questions
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Answer:
    """Structured answer with confidence and reasoning"""
    question_id: str
    answer: str
    type: str
    confidence: float
    reasoning: str


class ZyBooksSolver:
    """Solve zyBooks questions using semantic compression and statistical reasoning"""
    
    def __init__(self):
        self.answers = []
        
        # Statistical knowledge base
        self.stats_knowledge = {
            "mean": "average of all values",
            "median": "middle value when sorted",
            "mode": "most frequent value",
            "standard_deviation": "measure of spread",
            "68_rule": "68% within 1 std dev",
            "95_rule": "95% within 2 std dev",
            "99_rule": "99.7% within 3 std dev",
            "variance": "average squared deviation",
            "normal_distribution": "bell curve distribution",
            "correlation": "measure of linear relationship",
            "probability": "likelihood between 0 and 1",
        }
    
    def flamelang_compress(self, text: str) -> Dict[str, str]:
        """
        Apply FlameLang semantic compression
        Layers: English -> Hebrew -> Wave -> DNA
        """
        # English layer: Extract key terms
        key_terms = self._extract_key_terms(text.lower())
        
        # Hebrew layer: Find root logic pattern
        logic_pattern = self._find_logic_pattern(text.lower())
        
        # Wave layer: Calculate truth probability
        truth_prob = self._calculate_truth_probability(text.lower(), key_terms)
        
        # DNA layer: Emit boolean/value codon
        codon = "TRUE" if truth_prob > 0.5 else "FALSE"
        
        return {
            "english": ", ".join(key_terms),
            "hebrew": logic_pattern,
            "wave": f"{truth_prob:.2f}",
            "dna": codon
        }
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract key statistical/mathematical terms"""
        terms = []
        for key in self.stats_knowledge.keys():
            if key.replace("_", " ") in text or key.replace("_", "-") in text:
                terms.append(key)
        
        # Also look for numbers and percentages
        numbers = re.findall(r'\d+\.?\d*%?', text)
        terms.extend(numbers[:3])  # Limit to first 3 numbers
        
        return terms
    
    def _find_logic_pattern(self, text: str) -> str:
        """Identify the logical pattern in the question"""
        # Common question patterns
        if "true or false" in text or "true\nfalse" in text:
            return "binary_choice"
        elif "percentage" in text or "%" in text:
            return "numeric_proportion"
        elif "mean" in text and "median" in text:
            return "central_tendency_comparison"
        elif "standard deviation" in text:
            return "dispersion_measure"
        elif "probability" in text:
            return "likelihood_calculation"
        else:
            return "general_concept"
    
    def _calculate_truth_probability(self, text: str, key_terms: List[str]) -> float:
        """Calculate probability that a statement is true based on statistical knowledge"""
        # Start with neutral probability
        prob = 0.5
        
        # Statistical facts that increase/decrease probability
        if "always" in text or "never" in text:
            # Absolute statements are usually false in statistics
            prob = 0.2
        
        if "68" in text and "standard deviation" in text:
            # Empirical rule: 68-95-99.7
            prob = 0.95
        
        if "95" in text and "standard deviation" in text:
            prob = 0.95
        
        if "mean" in text and "median" in text and "greater" in text:
            # Mean is not always greater than median
            prob = 0.3
        
        if "normal distribution" in text and "bell" in text:
            prob = 0.9
        
        return prob
    
    def solve_true_false(self, question: Dict) -> Answer:
        """Solve true/false questions"""
        text = question["text"].lower()
        
        # Remove "true or false:" prefix if present to avoid false positives
        text_clean = re.sub(r'\btrue or false[:\s]+', '', text, flags=re.IGNORECASE)
        
        # Apply FlameLang compression
        compressed = self.flamelang_compress(text_clean)
        
        # Analyze common false patterns
        confidence = 0.7
        answer = "FALSE"
        reasoning = "Statistical default"
        
        # Check for known statistical facts first (highest priority)
        if "68" in text_clean and ("standard deviation" in text_clean or "std" in text_clean):
            # 68% within 1 standard deviation is TRUE
            if "one" in text_clean or "1" in text_clean:
                answer = "TRUE"
                confidence = 0.95
                reasoning = "68-95-99.7 empirical rule: 68% within 1 std dev"
            else:
                answer = "TRUE"
                confidence = 0.95
                reasoning = "68-95-99.7 empirical rule"
        
        elif "95" in text_clean and ("standard deviation" in text_clean or "std" in text_clean):
            # 95% within 2 standard deviations is TRUE
            answer = "TRUE"
            confidence = 0.95
            reasoning = "95% within 2 std deviations (empirical rule)"
        
        elif "99" in text_clean and ("standard deviation" in text_clean or "std" in text_clean):
            # 99.7% within 3 standard deviations is TRUE
            answer = "TRUE"
            confidence = 0.95
            reasoning = "99.7% within 3 std deviations (empirical rule)"
        
        elif "normal distribution" in text_clean and "symmetric" in text_clean:
            answer = "TRUE"
            confidence = 0.9
            reasoning = "Normal distributions are symmetric"
        
        # Check for absolute statements (usually false) - but only if not already matched above
        elif "always" in text_clean or "never" in text_clean:
            answer = "FALSE"
            confidence = 0.85
            reasoning = "Absolute statements are rarely true in statistics"
        
        elif "all" in text_clean or "none" in text_clean:
            # Be careful with "all" - it appears in "falls" etc.
            if re.search(r'\ball\b', text_clean) or re.search(r'\bnone\b', text_clean):
                answer = "FALSE"
                confidence = 0.85
                reasoning = "Absolute statements are rarely true in statistics"
        
        elif compressed["dna"] == "TRUE":
            answer = "TRUE"
            confidence = float(compressed["wave"])
            reasoning = f"FlameLang compression: {compressed['hebrew']}"
        
        return Answer(
            question_id=question["id"],
            answer=answer,
            type="true_false",
            confidence=confidence,
            reasoning=reasoning
        )
    
    def solve_multiple_choice(self, question: Dict) -> Answer:
        """Solve multiple choice questions"""
        text = question["text"].lower()
        options = question.get("options", [])
        
        confidence = 0.6
        answer = "b"
        reasoning = "Statistical heuristic"
        
        # Look for empirical rule questions
        # Check what the question is asking about
        asking_for_one_std = "one" in text or "1" in text or "first" in text
        asking_for_two_std = "two" in text or "2" in text or "second" in text
        asking_for_three_std = "three" in text or "3" in text or "third" in text
        
        # Check options for percentages
        options_str = str(options).lower()
        
        if ("standard deviation" in text or "std" in text) and options:
            if asking_for_two_std and "95" in options_str:
                # Looking for 2 std dev answer - should be 95%
                answer = next((opt for opt in options if "95" in opt), "b")
                confidence = 0.95
                reasoning = "Empirical rule: 95% within 2 std dev"
            elif asking_for_one_std and "68" in options_str:
                # Looking for 1 std dev answer - should be 68%
                answer = next((opt for opt in options if "68" in opt), "b")
                confidence = 0.95
                reasoning = "Empirical rule: 68% within 1 std dev"
            elif asking_for_three_std and "99" in options_str:
                # Looking for 3 std dev answer - should be 99.7%
                answer = next((opt for opt in options if "99" in opt), "d")
                confidence = 0.95
                reasoning = "Empirical rule: 99.7% within 3 std dev"
            elif "95" in options_str:
                # Default to 95% if asking about 2 std
                answer = next((opt for opt in options if "95" in opt), "b")
                confidence = 0.85
                reasoning = "Empirical rule: likely asking about 2 std dev"
            elif "68" in options_str:
                # Default to 68% if available
                answer = next((opt for opt in options if "68" in opt), "b")
                confidence = 0.85
                reasoning = "Empirical rule: likely asking about 1 std dev"
        
        # Extract just the letter from the option
        if isinstance(answer, str) and ")" in answer:
            answer = answer.split(")")[0]
        
        return Answer(
            question_id=question["id"],
            answer=answer,
            type="multiple_choice",
            confidence=confidence,
            reasoning=reasoning
        )
    
    def solve_numeric(self, question: Dict) -> Answer:
        """Solve numeric questions"""
        text = question["text"].lower()
        
        # Look for percentage patterns
        if "percentage" in text or "%" in text:
            if "68" in text or "one standard deviation" in text:
                answer = "68"
                confidence = 0.95
                reasoning = "Empirical rule"
            elif "95" in text or "two standard deviation" in text:
                answer = "95"
                confidence = 0.95
                reasoning = "Empirical rule"
            else:
                answer = "50"
                confidence = 0.5
                reasoning = "Default estimate"
        else:
            answer = "0"
            confidence = 0.3
            reasoning = "Insufficient information"
        
        return Answer(
            question_id=question["id"],
            answer=answer,
            type="numeric",
            confidence=confidence,
            reasoning=reasoning
        )
    
    def solve(self, questions: List[Dict]) -> List[Answer]:
        """Solve all questions"""
        self.answers = []
        
        for question in questions:
            q_type = question.get("type", "multiple_choice")
            
            if q_type == "true_false":
                answer = self.solve_true_false(question)
            elif q_type == "numeric":
                answer = self.solve_numeric(question)
            else:
                answer = self.solve_multiple_choice(question)
            
            self.answers.append(answer)
        
        return self.answers
    
    def get_answers(self) -> List[Dict]:
        """Get answers as dictionary list"""
        return [
            {
                "question_id": a.question_id,
                "answer": a.answer,
                "type": a.type,
                "confidence": a.confidence,
                "reasoning": a.reasoning
            }
            for a in self.answers
        ]


def main():
    """Test the solver"""
    sample_questions = [
        {
            "id": "q1",
            "type": "true_false",
            "text": "The mean is always greater than the median",
            "section": "1.5"
        },
        {
            "id": "q2",
            "type": "multiple_choice",
            "text": "What percentage within one standard deviation?",
            "options": ["a) 50%", "b) 68%", "c) 95%", "d) 99%"],
            "section": "1.5"
        }
    ]
    
    solver = ZyBooksSolver()
    answers = solver.solve(sample_questions)
    
    for answer in answers:
        print(f"{answer.question_id}: {answer.answer} (confidence: {answer.confidence})")
        print(f"  Reasoning: {answer.reasoning}\n")


if __name__ == "__main__":
    main()
