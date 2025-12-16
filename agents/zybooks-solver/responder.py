#!/usr/bin/env python3
"""
zyBooks Responder
Formats answers for operator in VESSEL MODE (minimal, direct, fast)
"""

import yaml
from typing import List, Dict
from solver import Answer


class ZyBooksResponder:
    """Formats answers in various output modes"""
    
    def __init__(self, answers: List[Answer], section: str = None):
        self.answers = answers
        self.section = section
    
    def to_yaml(self) -> str:
        """Format answers as YAML (primary format)"""
        data = {
            'section': self.section or 'unknown',
            'answers': {}
        }
        
        for answer in self.answers:
            data['answers'][answer.question_id] = {
                'answer': answer.answer,
                'type': answer.type,
                'confidence': round(answer.confidence, 2)
            }
        
        return yaml.dump(data, default_flow_style=False, sort_keys=False)
    
    def to_vessel_mode(self) -> str:
        """Format answers in VESSEL MODE - rapid fire, minimal"""
        lines = []
        lines.append(f"🔥 SECTION {self.section or '???'}")
        lines.append("")
        
        for answer in self.answers:
            # Format based on type
            if answer.type == 'true_false':
                symbol = "✓" if answer.answer == "TRUE" else "✗"
                lines.append(f"{answer.question_id}: {symbol} {answer.answer}")
            elif answer.type == 'numeric':
                lines.append(f"{answer.question_id}: {answer.answer}")
            elif answer.type == 'multiple_choice':
                lines.append(f"{answer.question_id}: ({answer.answer})")
            else:
                lines.append(f"{answer.question_id}: {answer.answer}")
        
        lines.append("")
        lines.append(f"Total: {len(self.answers)} answers")
        
        return "\n".join(lines)
    
    def to_detailed(self) -> str:
        """Format answers with reasoning (for debugging)"""
        lines = []
        lines.append(f"=== SECTION {self.section or 'UNKNOWN'} ===")
        lines.append("")
        
        for answer in self.answers:
            lines.append(f"{answer.question_id}: {answer.answer}")
            lines.append(f"  Type: {answer.type}")
            lines.append(f"  Confidence: {answer.confidence:.2%}")
            lines.append(f"  Reasoning: {answer.reasoning}")
            lines.append("")
        
        return "\n".join(lines)
    
    def to_json_compatible(self) -> Dict:
        """Format as JSON-compatible dict"""
        return {
            'section': self.section or 'unknown',
            'answers': [
                {
                    'id': ans.question_id,
                    'answer': ans.answer,
                    'type': ans.type,
                    'confidence': round(ans.confidence, 2),
                    'reasoning': ans.reasoning
                }
                for ans in self.answers
            ],
            'total': len(self.answers)
        }


def format_vessel_mode(answers: List[Answer], section: str = None) -> str:
    """Quick function for VESSEL MODE output"""
    responder = ZyBooksResponder(answers, section)
    return responder.to_vessel_mode()


def format_yaml(answers: List[Answer], section: str = None) -> str:
    """Quick function for YAML output"""
    responder = ZyBooksResponder(answers, section)
    return responder.to_yaml()


if __name__ == "__main__":
    from parser import parse_zybooks_content
    from solver import solve_questions
    
    sample = """
    Section 1.5 - Statistics Basics
    
    1) The mean is the average of a dataset.
    True
    False
    
    2) What is 25% of 80?
    [ ]
    
    3) Standard deviation measures spread.
    True
    False
    """
    
    questions = parse_zybooks_content(sample)
    answers = solve_questions(questions)
    
    print("=== VESSEL MODE ===")
    print(format_vessel_mode(answers, "1.5"))
    print("\n=== YAML FORMAT ===")
    print(format_yaml(answers, "1.5"))
