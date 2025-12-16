#!/usr/bin/env python3
"""
zyBooks MAT-243 Grade Calculator and Metrics Exporter
Tracks completion, calculates grades, and exports metrics
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple


class ZyBooksGradeCalculator:
    """Calculate grades and export metrics from zyBooks progress tracking"""
    
    def __init__(self, progress_file: str = "progress.json"):
        self.progress_file = Path(__file__).parent / progress_file
        self.progress = self._load_progress()
        
    def _load_progress(self) -> Dict:
        """Load progress data from JSON file"""
        with open(self.progress_file) as f:
            return json.load(f)
    
    def calculate_section_score(self, section_key: str) -> Tuple[float, int, int]:
        """
        Calculate score for a specific section
        
        Returns:
            Tuple of (percentage, completed, total)
        """
        section = self.progress["module_1"]["sections"][section_key]
        
        participation = section.get("participation_activities", 0)
        challenge = section.get("challenge_activities", 0)
        
        # Check for question-based tracking
        if "questions" in section:
            questions = section["questions"]
            completed = sum(1 for q in questions.values() 
                          if q.get("status") == "completed" and q.get("correct") is True)
            total = len([q for q in questions.values() if q.get("status") != "pending" or q.get("question") is not None])
            if total == 0:
                total = len(questions)
        else:
            completed = participation + challenge
            total = max(completed, 1)  # Avoid division by zero
        
        percentage = (completed / total * 100) if total > 0 else 0.0
        return percentage, completed, total
    
    def calculate_module_score(self) -> Dict:
        """Calculate overall module score"""
        sections = self.progress["module_1"]["sections"]
        
        total_score = 0.0
        section_count = 0
        completed_sections = 0
        
        section_scores = {}
        
        for section_key, section_data in sections.items():
            percentage, completed, total = self.calculate_section_score(section_key)
            section_scores[section_key] = {
                "name": section_data["name"],
                "percentage": percentage,
                "completed": completed,
                "total": total,
                "status": section_data["status"]
            }
            
            total_score += percentage
            section_count += 1
            
            if section_data["status"] == "completed":
                completed_sections += 1
        
        average_score = total_score / section_count if section_count > 0 else 0.0
        
        return {
            "module_name": self.progress["module_1"]["name"],
            "average_score": average_score,
            "completed_sections": completed_sections,
            "total_sections": section_count,
            "section_scores": section_scores
        }
    
    def export_metrics(self) -> Dict:
        """Export all metrics for grade tracking"""
        module_score = self.calculate_module_score()
        
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "course": self.progress["course"],
            "student": self.progress["student"],
            "semester": self.progress["semester"],
            "module_1": module_score,
            "overall": {
                "completion_percentage": self.progress["overall_progress"]["completion_percentage"],
                "dopamine_points": self.progress["overall_progress"]["total_dopamine_points"],
                "sections_completed": self.progress["overall_progress"]["completed_sections"],
                "sections_in_progress": self.progress["overall_progress"]["in_progress_sections"],
                "total_sections": self.progress["overall_progress"]["total_sections"]
            },
            "next_milestone": self.progress.get("next_milestone", "Continue progress"),
            "last_updated": self.progress.get("last_updated")
        }
        
        return metrics
    
    def generate_report(self) -> str:
        """Generate a human-readable progress report"""
        metrics = self.export_metrics()
        module = metrics["module_1"]
        
        report = []
        report.append("=" * 70)
        report.append(f"zyBooks Progress Report - {metrics['course']}")
        report.append("=" * 70)
        report.append(f"Student: {metrics['student']}")
        report.append(f"Semester: {metrics['semester']}")
        report.append(f"Generated: {metrics['timestamp']}")
        report.append("")
        report.append(f"Module 1: {module['module_name']}")
        report.append(f"  Overall Score: {module['average_score']:.2f}%")
        report.append(f"  Progress: {module['completed_sections']}/{module['total_sections']} sections completed")
        report.append(f"  Dopamine Points: 🔥 x {metrics['overall']['dopamine_points']}")
        report.append("")
        report.append("Section Breakdown:")
        report.append("-" * 70)
        
        for section_key, section in module["section_scores"].items():
            status_emoji = {
                "completed": "✅",
                "in_progress": "🔄",
                "not_started": "⭕"
            }.get(section["status"], "❓")
            
            report.append(f"{status_emoji} {section_key}: {section['name']}")
            report.append(f"   Score: {section['percentage']:.1f}% ({section['completed']}/{section['total']})")
        
        report.append("")
        report.append(f"Next Milestone: {metrics['next_milestone']}")
        report.append("=" * 70)
        
        return "\n".join(report)
    
    def save_metrics(self, output_file: str = "grade_metrics.json"):
        """Save metrics to JSON file"""
        metrics = self.export_metrics()
        output_path = Path(__file__).parent / output_file
        
        with open(output_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        print(f"Metrics exported to: {output_path}")
        return output_path


def main():
    """Main entry point for grade calculator"""
    calculator = ZyBooksGradeCalculator()
    
    # Generate and print report
    report = calculator.generate_report()
    print(report)
    
    # Save metrics
    calculator.save_metrics()
    
    # Return metrics for programmatic access
    return calculator.export_metrics()


if __name__ == "__main__":
    main()
