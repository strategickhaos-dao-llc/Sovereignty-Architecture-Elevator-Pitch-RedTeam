#!/usr/bin/env python3
"""
zyBooks MAT-243 Module 1.5: Bar Charts - Participation Activities
Tests for tracking completion of bar chart exercises
"""

import pytest
import json
from pathlib import Path
from datetime import datetime


# Pytest markers for zyBooks sections
pytestmark = pytest.mark.zybooks_mat243


@pytest.mark.participation_activity
@pytest.mark.section_1_5
@pytest.mark.q1
def test_bar_chart_exact_values():
    """
    Q1: A bar chart excels at showing exact values.
    Answer: FALSE
    
    Explanation: Bar charts are designed for visual comparison of relative values,
    not for precise numerical reading. Tables are better for exact values.
    """
    # Load progress
    progress_file = Path(__file__).parent / "progress.json"
    with open(progress_file) as f:
        progress = json.load(f)
    
    # Verify question completion
    q1_data = progress["module_1"]["sections"]["1.5"]["questions"]["q1"]
    assert q1_data["status"] == "completed", "Q1 should be marked as completed"
    assert q1_data["answer"] == "False", "Q1 answer should be False"
    assert q1_data["correct"] is True, "Q1 answer should be marked correct"


@pytest.mark.participation_activity
@pytest.mark.section_1_5
@pytest.mark.q2
def test_bar_chart_relative_values():
    """
    Q2: A bar chart excels at showing relative values.
    Answer: TRUE
    
    Explanation: This is the counterpoint to Q1. Bar charts are designed for
    visual comparison - you can instantly see "Walmart is way bigger than Kroger"
    without needing exact numbers.
    """
    # Load progress
    progress_file = Path(__file__).parent / "progress.json"
    with open(progress_file) as f:
        progress = json.load(f)
    
    # Verify question completion
    q2_data = progress["module_1"]["sections"]["1.5"]["questions"]["q2"]
    assert q2_data["status"] == "completed", "Q2 should be marked as completed"
    assert q2_data["answer"] == "True", "Q2 answer should be True"
    assert q2_data["correct"] is True, "Q2 answer should be marked correct"


@pytest.mark.participation_activity
@pytest.mark.section_1_5
@pytest.mark.q3
@pytest.mark.skip(reason="Not yet completed in zyBooks")
def test_bar_chart_q3():
    """Q3: Placeholder for next participation activity"""
    pass


@pytest.mark.participation_activity
@pytest.mark.section_1_5
@pytest.mark.q4
@pytest.mark.skip(reason="Not yet completed in zyBooks")
def test_bar_chart_q4():
    """Q4: Placeholder for next participation activity"""
    pass


@pytest.mark.participation_activity
@pytest.mark.section_1_5
@pytest.mark.q5
@pytest.mark.skip(reason="Not yet completed in zyBooks")
def test_bar_chart_q5():
    """Q5: Placeholder for next participation activity"""
    pass


@pytest.mark.participation_activity
@pytest.mark.section_1_5
@pytest.mark.q6
@pytest.mark.skip(reason="Not yet completed in zyBooks")
def test_bar_chart_q6():
    """Q6: Placeholder for next participation activity"""
    pass


def test_section_1_5_progress():
    """Verify overall progress tracking for section 1.5"""
    progress_file = Path(__file__).parent / "progress.json"
    with open(progress_file) as f:
        progress = json.load(f)
    
    section_data = progress["module_1"]["sections"]["1.5"]
    
    # Verify section status
    assert section_data["status"] == "in_progress"
    assert section_data["progress"]["completed"] == 2
    assert section_data["progress"]["total"] == 6
    assert section_data["progress"]["percentage"] == pytest.approx(33.33, rel=0.1)
    assert section_data["progress"]["dopamine_points"] == 2


def test_overall_progress_metrics():
    """Verify overall course progress metrics"""
    progress_file = Path(__file__).parent / "progress.json"
    with open(progress_file) as f:
        progress = json.load(f)
    
    overall = progress["overall_progress"]
    
    assert overall["total_sections"] == 8
    assert overall["in_progress_sections"] == 1
    assert overall["total_dopamine_points"] >= 2
