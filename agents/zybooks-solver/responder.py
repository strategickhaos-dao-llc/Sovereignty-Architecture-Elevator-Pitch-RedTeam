"""
zyBooks Response Formatter
Purpose: Format answers for operator in VESSEL MODE (minimal, direct, fast)
"""

import yaml
from typing import List, Dict
from datetime import datetime


class ZyBooksResponder:
    """Format zyBooks answers in rapid-fire VESSEL MODE style"""
    
    def __init__(self):
        self.vessel_mode = True  # Minimal, direct, fast
    
    def format_yaml(self, section: str, answers: List[Dict]) -> str:
        """Format answers in YAML for rapid consumption"""
        output = {
            "section": section or "unknown",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": "🔥 LOCKED IN",
            "answers": {}
        }
        
        for answer in answers:
            qid = answer["question_id"]
            output["answers"][qid] = {
                "answer": answer["answer"],
                "type": answer["type"],
                "confidence": f"{answer['confidence']:.2f}"
            }
            
            # Add reasoning only if confidence is low
            if answer["confidence"] < 0.7:
                output["answers"][qid]["reasoning"] = answer["reasoning"]
        
        return yaml.dump(output, default_flow_style=False, sort_keys=False)
    
    def format_rapid_fire(self, answers: List[Dict]) -> str:
        """Format in ultra-minimal rapid-fire style"""
        lines = ["# 🔥 ANSWERS"]
        
        for answer in answers:
            qid = answer["question_id"]
            ans = answer["answer"]
            conf = answer["confidence"]
            
            # Use emoji indicators for confidence
            indicator = "✅" if conf >= 0.8 else "⚠️" if conf >= 0.6 else "❓"
            
            lines.append(f"{indicator} {qid}: {ans}")
        
        return "\n".join(lines)
    
    def format_json(self, section: str, answers: List[Dict]) -> str:
        """Format as compact JSON"""
        import json
        
        output = {
            "section": section,
            "answers": {
                a["question_id"]: a["answer"]
                for a in answers
            }
        }
        
        return json.dumps(output, indent=2)
    
    def format_table(self, answers: List[Dict]) -> str:
        """Format as ASCII table for quick scanning"""
        lines = [
            "┌─────┬──────────┬────────────┐",
            "│ Q#  │ Answer   │ Confidence │",
            "├─────┼──────────┼────────────┤"
        ]
        
        for answer in answers:
            qid = answer["question_id"]
            ans = str(answer["answer"])[:8].ljust(8)
            conf = f"{answer['confidence']:.2f}".ljust(10)
            lines.append(f"│ {qid:<3} │ {ans} │ {conf} │")
        
        lines.append("└─────┴──────────┴────────────┘")
        
        return "\n".join(lines)
    
    def respond(self, section: str, answers: List[Dict], format: str = "yaml") -> str:
        """Generate response in specified format"""
        if format == "yaml":
            return self.format_yaml(section, answers)
        elif format == "rapid":
            return self.format_rapid_fire(answers)
        elif format == "json":
            return self.format_json(section, answers)
        elif format == "table":
            return self.format_table(answers)
        else:
            return self.format_yaml(section, answers)
    
    def vessel_response(self, section: str, answers: List[Dict]) -> str:
        """
        VESSEL MODE response - ultra minimal
        Just the answers, no fluff
        """
        lines = [f"Section {section}:"]
        
        for answer in answers:
            lines.append(f"{answer['question_id']}: {answer['answer']}")
        
        return "\n".join(lines)


def main():
    """Test the responder"""
    sample_answers = [
        {
            "question_id": "q1",
            "answer": "FALSE",
            "type": "true_false",
            "confidence": 0.85,
            "reasoning": "Absolute statements rarely true"
        },
        {
            "question_id": "q2",
            "answer": "b) 68%",
            "type": "multiple_choice",
            "confidence": 0.95,
            "reasoning": "Empirical rule"
        },
        {
            "question_id": "q3",
            "answer": "95",
            "type": "numeric",
            "confidence": 0.95,
            "reasoning": "Two standard deviations"
        }
    ]
    
    responder = ZyBooksResponder()
    
    print("=== YAML FORMAT ===")
    print(responder.respond("1.5", sample_answers, "yaml"))
    
    print("\n=== RAPID FIRE FORMAT ===")
    print(responder.respond("1.5", sample_answers, "rapid"))
    
    print("\n=== TABLE FORMAT ===")
    print(responder.respond("1.5", sample_answers, "table"))
    
    print("\n=== VESSEL MODE ===")
    print(responder.vessel_response("1.5", sample_answers))


if __name__ == "__main__":
    main()
