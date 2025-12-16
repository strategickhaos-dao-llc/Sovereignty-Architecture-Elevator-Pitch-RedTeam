#!/usr/bin/env python3
"""
zyBooks Content Parser
Extracts question blocks from pasted zyBooks content
"""

import re
import json
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class Question:
    """Represents a parsed zyBooks question"""
    id: str
    type: str  # true_false | multiple_choice | fill_blank | numeric
    text: str
    options: Optional[List[str]] = None
    section: Optional[str] = None


class ZyBooksParser:
    """Parser for zyBooks content"""
    
    # Detection patterns
    MARKERS = [
        "participation activity",
        "zyBooks",
        "Check Show answer",
        "Feedback?",
        "challenge activity",
        "Section 1.",
        "True\nFalse"
    ]
    
    # Content structure patterns
    PATTERNS = {
        'numbered_question': re.compile(r'^\d+\)\s+(.*?)(?=^\d+\)|$)', re.MULTILINE | re.DOTALL),
        'true_false': re.compile(r'\b(True|False)\b'),
        'fill_blank': re.compile(r'\[\s*\]'),
        'percentage': re.compile(r'\s*%\s*'),
        'section': re.compile(r'Section\s+(\d+\.[\d.]+)'),
        'url': re.compile(r'learn\.zybooks\.com/zybook/')
    }
    
    def __init__(self):
        self.questions: List[Question] = []
        
    def detect_zybooks_content(self, content: str) -> bool:
        """Detect if content is from zyBooks"""
        marker_count = sum(1 for marker in self.MARKERS if marker.lower() in content.lower())
        url_match = self.PATTERNS['url'].search(content)
        
        return marker_count >= 2 or url_match is not None
    
    def extract_section(self, content: str) -> Optional[str]:
        """Extract section number from content"""
        match = self.PATTERNS['section'].search(content)
        return match.group(1) if match else None
    
    def detect_question_type(self, text: str) -> str:
        """Detect the type of question"""
        # Check order matters - more specific patterns first
        if 'True' in text and 'False' in text:
            return 'true_false'
        elif re.search(r'\d+\.?\d*\s*%', text):
            # Numeric with percentage - even if has fill blank
            return 'numeric'
        elif re.search(r'^[a-d]\)', text, re.MULTILINE | re.IGNORECASE):
            return 'multiple_choice'
        elif self.PATTERNS['fill_blank'].search(text):
            return 'fill_blank'
        else:
            return 'text'
    
    def parse(self, content: str) -> List[Question]:
        """Parse zyBooks content into structured questions"""
        if not self.detect_zybooks_content(content):
            return []
        
        section = self.extract_section(content)
        questions = []
        
        # Split content into blocks separated by empty lines
        blocks = re.split(r'\n\s*\n', content)
        
        # Filter to only blocks that start with numbered questions
        question_blocks = [b.strip() for b in blocks if re.match(r'^\d+\)', b.strip())]
        
        for idx, block in enumerate(question_blocks, 1):
            # Extract question number and text
            match = re.match(r'^(\d+\)\s+)(.*)', block, re.DOTALL)
            if not match:
                continue
            
            question_text = match.group(2).strip()
            
            if not question_text or len(question_text) < 3:
                continue
            
            q_type = self.detect_question_type(question_text)
            
            # Extract options for multiple choice
            options = None
            if q_type == 'multiple_choice':
                options = re.findall(r'^([a-d]\).*?)(?=^[a-d]\)|$)', 
                                    question_text, 
                                    re.MULTILINE | re.IGNORECASE)
            
            question = Question(
                id=f"q{idx}",
                type=q_type,
                text=question_text,
                options=options,
                section=section
            )
            
            questions.append(question)
        
        self.questions = questions
        return questions
    
    def to_json(self, filepath: str = None) -> str:
        """Export questions to JSON format"""
        data = {
            'questions': [asdict(q) for q in self.questions],
            'total': len(self.questions)
        }
        
        json_str = json.dumps(data, indent=2)
        
        if filepath:
            with open(filepath, 'w') as f:
                f.write(json_str)
        
        return json_str


def parse_zybooks_content(content: str) -> List[Question]:
    """Convenience function to parse zyBooks content"""
    parser = ZyBooksParser()
    return parser.parse(content)


if __name__ == "__main__":
    # Test with sample content
    sample = """
    Section 1.5
    
    1) The mean is the average of a dataset.
    True
    False
    
    2) What is 50% of 100?
    [ ]
    
    3) Standard deviation measures:
    a) Central tendency
    b) Spread of data
    c) Mode
    d) Median
    """
    
    parser = ZyBooksParser()
    questions = parser.parse(sample)
    
    print("Detected questions:")
    for q in questions:
        print(f"  {q.id}: {q.type} - {q.text[:50]}...")
