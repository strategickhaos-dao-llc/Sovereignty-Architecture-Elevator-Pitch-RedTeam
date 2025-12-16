#!/usr/bin/env python3
"""
zyBooks Solver
Applies FlameLang logic and statistical reasoning to solve questions
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from parser import Question


@dataclass
class Answer:
    """Represents an answer to a question"""
    question_id: str
    answer: str
    confidence: float  # 0.0 to 1.0
    reasoning: str
    type: str


class ZyBooksSolver:
    """Solver for zyBooks questions using FlameLang semantic compression"""
    
    # Statistical and mathematical knowledge base
    KNOWLEDGE_BASE = {
        'mean': 'average of dataset',
        'median': 'middle value when sorted',
        'mode': 'most frequent value',
        'standard deviation': 'measure of spread',
        'variance': 'square of standard deviation',
        'normal distribution': 'bell curve',
        'probability': 'likelihood between 0 and 1',
        'sample': 'subset of population',
        'population': 'entire dataset',
        'hypothesis': 'testable statement',
        'null hypothesis': 'no effect statement',
        'p-value': 'probability of observing data given null',
        'correlation': 'relationship between variables',
        'regression': 'prediction model',
        'outlier': 'extreme value'
    }
    
    # Common true/false patterns
    TRUE_PATTERNS = [
        r'mean.*average',
        r'median.*middle',
        r'mode.*most.*frequent',
        r'standard deviation.*spread',
        r'variance.*deviation.*squared',
        r'probability.*between.*0.*1',
        r'sample.*subset',
        r'correlation.*relationship'
    ]
    
    FALSE_PATTERNS = [
        r'mean.*median',  # mean is NOT median
        r'standard deviation.*average',  # std dev is NOT average
        r'correlation.*causation',  # correlation does NOT imply causation
        r'variance.*standard deviation$'  # variance is NOT std dev (it's squared)
    ]
    
    def __init__(self):
        self.answers: List[Answer] = []
    
    def solve_true_false(self, question: Question) -> Answer:
        """Solve true/false questions using pattern matching"""
        text_lower = question.text.lower()
        
        # Check for TRUE patterns
        true_score = sum(1 for pattern in self.TRUE_PATTERNS 
                        if re.search(pattern, text_lower, re.IGNORECASE))
        
        # Check for FALSE patterns
        false_score = sum(1 for pattern in self.FALSE_PATTERNS 
                         if re.search(pattern, text_lower, re.IGNORECASE))
        
        # Check knowledge base
        for term, definition in self.KNOWLEDGE_BASE.items():
            if term in text_lower and definition in text_lower:
                true_score += 2
        
        # Determine answer
        if true_score > false_score:
            answer_value = "TRUE"
            confidence = min(0.9, 0.6 + (true_score * 0.1))
            reasoning = f"Pattern match: {true_score} true indicators"
        elif false_score > true_score:
            answer_value = "FALSE"
            confidence = min(0.9, 0.6 + (false_score * 0.1))
            reasoning = f"Pattern match: {false_score} false indicators"
        else:
            answer_value = "TRUE"  # Default to TRUE if uncertain
            confidence = 0.5
            reasoning = "No clear pattern, defaulting to TRUE"
        
        return Answer(
            question_id=question.id,
            answer=answer_value,
            confidence=confidence,
            reasoning=reasoning,
            type="true_false"
        )
    
    def solve_numeric(self, question: Question) -> Answer:
        """Solve numeric questions using mathematical evaluation"""
        text = question.text
        
        # Extract numbers from question
        numbers = re.findall(r'\d+\.?\d*', text)
        
        # Look for percentage calculations
        if '%' in text and 'of' in text.lower():
            try:
                percent = float(numbers[0])
                value = float(numbers[1])
                result = (percent / 100) * value
                return Answer(
                    question_id=question.id,
                    answer=str(result),
                    confidence=0.95,
                    reasoning=f"{percent}% of {value}",
                    type="numeric"
                )
            except (IndexError, ValueError):
                pass
        
        # Default numeric answer
        return Answer(
            question_id=question.id,
            answer="0",
            confidence=0.3,
            reasoning="Unable to determine calculation",
            type="numeric"
        )
    
    def solve_multiple_choice(self, question: Question) -> Answer:
        """Solve multiple choice using semantic analysis"""
        if not question.options:
            return Answer(
                question_id=question.id,
                answer="a",
                confidence=0.3,
                reasoning="No options provided",
                type="multiple_choice"
            )
        
        # Score each option based on knowledge base
        scores = []
        for idx, option in enumerate(question.options):
            score = 0
            option_lower = option.lower()
            
            # Check against knowledge base
            for term, definition in self.KNOWLEDGE_BASE.items():
                if term in question.text.lower() and definition in option_lower:
                    score += 3
                elif term in option_lower:
                    score += 1
            
            scores.append((idx, score, option))
        
        # Select highest scoring option
        best = max(scores, key=lambda x: x[1])
        
        answer_letter = chr(ord('a') + best[0])
        confidence = min(0.9, 0.5 + (best[1] * 0.1))
        
        return Answer(
            question_id=question.id,
            answer=answer_letter,
            confidence=confidence,
            reasoning=f"Semantic score: {best[1]}",
            type="multiple_choice"
        )
    
    def solve_fill_blank(self, question: Question) -> Answer:
        """Solve fill-in-the-blank questions"""
        text_lower = question.text.lower()
        
        # Look for mathematical terms
        for term in self.KNOWLEDGE_BASE.keys():
            if term in text_lower:
                return Answer(
                    question_id=question.id,
                    answer=term,
                    confidence=0.7,
                    reasoning=f"Keyword match: {term}",
                    type="fill_blank"
                )
        
        return Answer(
            question_id=question.id,
            answer="unknown",
            confidence=0.3,
            reasoning="No clear term identified",
            type="fill_blank"
        )
    
    def solve(self, questions: List[Question]) -> List[Answer]:
        """Solve all questions"""
        self.answers = []
        
        for question in questions:
            if question.type == 'true_false':
                answer = self.solve_true_false(question)
            elif question.type == 'numeric':
                answer = self.solve_numeric(question)
            elif question.type == 'multiple_choice':
                answer = self.solve_multiple_choice(question)
            elif question.type == 'fill_blank':
                answer = self.solve_fill_blank(question)
            else:
                answer = Answer(
                    question_id=question.id,
                    answer="unknown",
                    confidence=0.1,
                    reasoning="Unknown question type",
                    type=question.type
                )
            
            self.answers.append(answer)
        
        return self.answers


def solve_questions(questions: List[Question]) -> List[Answer]:
    """Convenience function to solve questions"""
    solver = ZyBooksSolver()
    return solver.solve(questions)


if __name__ == "__main__":
    from parser import parse_zybooks_content
    
    sample = """
    Section 1.5
    
    1) The mean is the average of a dataset.
    True
    False
    
    2) What is 25% of 80?
    [ ]
    """
    
    questions = parse_zybooks_content(sample)
    answers = solve_questions(questions)
    
    print("\nAnswers:")
    for ans in answers:
        print(f"  {ans.question_id}: {ans.answer} (confidence: {ans.confidence:.2f})")
        print(f"    Reasoning: {ans.reasoning}")
