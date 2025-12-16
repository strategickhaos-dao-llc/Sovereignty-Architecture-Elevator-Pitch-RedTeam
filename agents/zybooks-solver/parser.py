"""
zyBooks Content Parser
Purpose: Parse pasted zyBooks content into structured format
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class Question:
    """Structured representation of a zyBooks question"""
    id: str
    type: str  # true_false, multiple_choice, fill_blank, numeric
    text: str
    options: Optional[List[str]] = None
    section: Optional[str] = None


class ZyBooksParser:
    """Parse zyBooks content into structured questions"""
    
    # Detection patterns
    MARKERS = [
        "participation activity",
        "zybooks",
        "check show answer",
        "feedback?",
        "challenge activity",
        "section ",
    ]
    
    URL_PATTERN = r"learn\.zybooks\.com/zybook/"
    
    # Content structure patterns
    NUMBERED_QUESTION = r"^(\d+)\)\s*(.+)"
    TRUE_FALSE = r"\b(True|False)\b"
    FILL_BLANK = r"\[[\s_]*\]"
    PERCENTAGE = r"\s*%\s*"
    SECTION_PATTERN = r"[Ss]ection\s+(\d+\.?\d*\.?\d*)"
    
    def __init__(self):
        self.questions = []
        self.section = None
        
    def is_zybooks_content(self, text: str) -> bool:
        """Detect if the text contains zyBooks content"""
        text_lower = text.lower()
        
        # Check for markers
        marker_count = sum(1 for marker in self.MARKERS if marker in text_lower)
        
        # Check for URL pattern
        has_url = bool(re.search(self.URL_PATTERN, text))
        
        # Check for content structure patterns
        has_numbered = bool(re.search(self.NUMBERED_QUESTION, text, re.MULTILINE))
        has_tf = bool(re.search(self.TRUE_FALSE, text))
        
        # Consider it zyBooks content if it has markers or structural patterns
        return marker_count >= 2 or has_url or (has_numbered and has_tf)
    
    def extract_section(self, text: str) -> Optional[str]:
        """Extract section number from content"""
        match = re.search(self.SECTION_PATTERN, text, re.IGNORECASE)
        if match:
            return match.group(1)
        return None
    
    def detect_question_type(self, text: str, options: Optional[List[str]] = None) -> str:
        """Detect the type of question based on content"""
        # Check for True/False pattern in text or options
        combined = text
        if options:
            combined = text + "\n" + "\n".join(options)
        
        # Look for True/False in question or options
        if re.search(r"\b(True|False)\b", combined, re.IGNORECASE):
            # Check if it's a true/false question (has both True and False)
            has_true = bool(re.search(r"\bTrue\b", combined, re.IGNORECASE))
            has_false = bool(re.search(r"\bFalse\b", combined, re.IGNORECASE))
            if has_true and has_false:
                return "true_false"
        
        # Check for fill in the blank
        if re.search(self.FILL_BLANK, text):
            return "fill_blank"
        
        # Check for numeric (contains numbers or percentages)
        if re.search(r"\d+\.?\d*\s*%?", text) and re.search(self.PERCENTAGE, text):
            return "numeric"
        
        # Check for multiple choice (has letters followed by text)
        if options and len(options) > 0:
            return "multiple_choice"
        
        # Default to multiple choice
        return "multiple_choice"
    
    def parse_question_block(self, block: str, question_num: int) -> Optional[Question]:
        """Parse a single question block"""
        lines = block.strip().split('\n')
        if not lines:
            return None
        
        # Extract question text and options
        question_text = []
        options = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if it's an option (a), b), c), d), etc.)
            option_match = re.match(r"^([a-d])\)\s*(.+)", line, re.IGNORECASE)
            if option_match:
                options.append(f"{option_match.group(1)}) {option_match.group(2)}")
            elif not re.match(r"^\d+\)", line):
                question_text.append(line)
        
        if not question_text:
            return None
        
        full_text = " ".join(question_text)
        q_type = self.detect_question_type(full_text, options)
        
        return Question(
            id=f"q{question_num}",
            type=q_type,
            text=full_text,
            options=options if options else None,
            section=self.section
        )
    
    def parse(self, content: str) -> Dict:
        """Parse zyBooks content into structured format"""
        if not self.is_zybooks_content(content):
            return {
                "error": "Content does not appear to be zyBooks format",
                "detected": False
            }
        
        # Extract section
        self.section = self.extract_section(content)
        
        # Split content into question blocks
        # Look for numbered questions like "1)", "2)", etc.
        question_blocks = re.split(r'\n\s*(\d+)\)\s*', content)
        
        self.questions = []
        
        # Process question blocks
        i = 1
        while i < len(question_blocks):
            if i + 1 < len(question_blocks):
                question_num = question_blocks[i]
                question_content = question_blocks[i + 1]
                
                question = self.parse_question_block(
                    question_content, 
                    int(question_num) if question_num.isdigit() else len(self.questions) + 1
                )
                
                if question:
                    self.questions.append(question)
                
                i += 2
            else:
                i += 1
        
        return {
            "detected": True,
            "section": self.section,
            "question_count": len(self.questions),
            "questions": [asdict(q) for q in self.questions]
        }
    
    def to_json(self) -> str:
        """Export questions to JSON format"""
        return json.dumps(
            [asdict(q) for q in self.questions],
            indent=2
        )
    
    def save_to_file(self, filepath: str):
        """Save parsed questions to file"""
        with open(filepath, 'w') as f:
            f.write(self.to_json())


def main():
    """Test the parser with sample content"""
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
    """
    
    parser = ZyBooksParser()
    result = parser.parse(sample_content)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
