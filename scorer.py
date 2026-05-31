#!/usr/bin/env python3
"""
Scoring engine for NUQRO – calculates raw scores, sub‑scores, and age‑normalised adjusted scores.

Uses norm tables (data/norms.json) for Z‑score transformation.
If norm file is missing, it creates a sensible default.
"""

import json
import os
from pathlib import Path
from questions import IQ_QUESTIONS, EQ_QUESTIONS, SQ_QUESTIONS, AQ_QUESTIONS   # <-- FIXED

# ---------- Norm loading and helpers ----------
NORMS_FILE = Path("data/norms.json")

def load_norms():
    """Load norm table from JSON; create default if missing or invalid."""
    if not NORMS_FILE.exists():
        return _create_default_norms()

    try:
        with open(NORMS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        # Norm file is empty or corrupted; recreate defaults.
        return _create_default_norms()


def _create_default_norms():
    default_norms = {
        "IQ": {
            "10-12": {"mean": 35, "sd": 8},
            "13-15": {"mean": 38, "sd": 8},
            "16-18": {"mean": 42, "sd": 8},
            "19-25": {"mean": 45, "sd": 9},
            "26-35": {"mean": 47, "sd": 9},
            "36-50": {"mean": 48, "sd": 9},
            "51+": {"mean": 46, "sd": 10}
        },
        "EQ": {
            "10-12": {"mean": 45, "sd": 10},
            "13-15": {"mean": 48, "sd": 10},
            "16-18": {"mean": 52, "sd": 11},
            "19-25": {"mean": 55, "sd": 11},
            "26-35": {"mean": 58, "sd": 11},
            "36-50": {"mean": 60, "sd": 12},
            "51+": {"mean": 62, "sd": 12}
        },
        "SQ": {
            "10-12": {"mean": 40, "sd": 9},
            "13-15": {"mean": 44, "sd": 9},
            "16-18": {"mean": 48, "sd": 10},
            "19-25": {"mean": 52, "sd": 10},
            "26-35": {"mean": 55, "sd": 10},
            "36-50": {"mean": 57, "sd": 11},
            "51+": {"mean": 58, "sd": 11}
        },
        "AQ": {
            "10-12": {"mean": 42, "sd": 11},
            "13-15": {"mean": 45, "sd": 11},
            "16-18": {"mean": 48, "sd": 11},
            "19-25": {"mean": 52, "sd": 12},
            "26-35": {"mean": 55, "sd": 12},
            "36-50": {"mean": 57, "sd": 12},
            "51+": {"mean": 58, "sd": 13}
        }
    }
    NORMS_FILE.parent.mkdir(exist_ok=True)
    with open(NORMS_FILE, "w") as f:
        json.dump(default_norms, f, indent=4)
    return default_norms

def get_age_group(age, norms, test_type):
    """Return the age group key (e.g., '19-25') for given age."""
    for group in norms[test_type].keys():
        if group == "51+":
            low, high = 51, 200
        else:
            low, high = map(int, group.split("-"))
        if low <= age <= high:
            return group
    return "51+"  # fallback

def compute_adjusted_score(raw_0_100, age, test_type):
    """
    Convert raw score (0-100) to age‑normalised adjusted score using Z‑score.
    For IQ: target mean=100, SD=15. For others: target mean=50, SD=15 (clamped 0-100).
    """
    norms = load_norms()
    group = get_age_group(age, norms, test_type)
    mean_norm = norms[test_type][group]["mean"]
    sd_norm = norms[test_type][group]["sd"]
    
    if sd_norm == 0:
        z = 0
    else:
        z = (raw_0_100 - mean_norm) / sd_norm
    
    if test_type == "IQ":
        # Standard IQ scale: mean 100, SD 15
        adjusted = 100 + (z * 15)
        return int(round(adjusted))
    else:
        # For EQ, SQ, AQ: scale to 0-100 with approximate mean 50, SD 15
        adjusted = 50 + (z * 15)
        # Clamp to 0-100
        adjusted = max(0, min(100, adjusted))
        return int(round(adjusted))

# ---------- Scoring for each test type ----------
def score_iq(answers, questions):
    """IQ: correct answers only."""
    total = len(questions)
    if total == 0:
        return {"raw_score": 0, "adjusted_score": 0}
    
    correct = 0
    for q in questions:
        qid = q['id']
        user_ans = answers.get(qid, "")
        if user_ans and user_ans == q.get('correct', ''):
            correct += 1
    
    raw_0_100 = (correct / total) * 100
    return {
        "raw_score": correct,           # raw number correct
        "raw_percent": raw_0_100,       # for internal use
        "adjusted_score": None          # to be filled later
    }

def score_eq(answers, questions):
    """EQ: Likert scale (1-5). Sub‑scores per dimension."""
    if not questions:
        return {"raw_score": 0, "adjusted_score": 0, "sub_scores": {}}
    
    dim_sums = {}
    dim_counts = {}
    total_points = 0
    total_questions = 0
    
    for q in questions:
        qid = q['id']
        user_ans = answers.get(qid, "")
        # Default to neutral (3) if skipped or invalid
        if user_ans not in ['A','B','C','D']:
            points = 3
        else:
            points = q['scores'].get(user_ans, 3)
        
        total_points += points
        total_questions += 1
        
        dim = q.get('dimension', 'unknown')
        dim_sums[dim] = dim_sums.get(dim, 0) + points
        dim_counts[dim] = dim_counts.get(dim, 0) + 1
    
    # Raw score 0-100
    min_possible = total_questions * 1
    max_possible = total_questions * 5
    if max_possible == min_possible:
        raw_0_100 = 50
    else:
        raw_0_100 = ((total_points - min_possible) / (max_possible - min_possible)) * 100
        raw_0_100 = max(0, min(100, raw_0_100))
    
    # Sub‑scores per dimension (0-100)
    sub_scores = {}
    for dim, sum_pts in dim_sums.items():
        count = dim_counts[dim]
        avg = sum_pts / count
        # Convert 1-5 to 0-100
        sub = ((avg - 1) / 4) * 100
        sub = max(0, min(100, sub))
        sub_scores[dim] = int(round(sub))
    
    return {
        "raw_score": int(round(raw_0_100)),
        "raw_points": total_points,
        "sub_scores": sub_scores,
        "adjusted_score": None
    }

def score_sq(answers, questions):
    """SQ: Likert scale (1-5). Sub‑scores per factor (social_acting, social_cognising, social_relating)."""
    if not questions:
        return {"raw_score": 0, "adjusted_score": 0, "sub_scores": {}}
    
    factor_sums = {}
    factor_counts = {}
    total_points = 0
    total_questions = 0
    
    for q in questions:
        qid = q['id']
        user_ans = answers.get(qid, "")
        if user_ans not in ['A','B','C','D']:
            points = 3
        else:
            points = q['scores'].get(user_ans, 3)
        
        total_points += points
        total_questions += 1
        
        factor = q.get('factor', 'unknown')
        factor_sums[factor] = factor_sums.get(factor, 0) + points
        factor_counts[factor] = factor_counts.get(factor, 0) + 1
    
    min_possible = total_questions * 1
    max_possible = total_questions * 5
    if max_possible == min_possible:
        raw_0_100 = 50
    else:
        raw_0_100 = ((total_points - min_possible) / (max_possible - min_possible)) * 100
        raw_0_100 = max(0, min(100, raw_0_100))
    
    sub_scores = {}
    for factor, sum_pts in factor_sums.items():
        count = factor_counts[factor]
        avg = sum_pts / count
        sub = ((avg - 1) / 4) * 100
        sub = max(0, min(100, sub))
        sub_scores[factor] = int(round(sub))
    
    return {
        "raw_score": int(round(raw_0_100)),
        "raw_points": total_points,
        "sub_scores": sub_scores,
        "adjusted_score": None
    }

def score_aq(answers, questions):
    """AQ: Likert scale (1-5). Sub‑scores per CORE dimension (Control, Ownership, Reach, Endurance)."""
    if not questions:
        return {"raw_score": 0, "adjusted_score": 0, "sub_scores": {}}
    
    dim_sums = {}
    dim_counts = {}
    total_points = 0
    total_questions = 0
    
    for q in questions:
        qid = q['id']
        user_ans = answers.get(qid, "")
        if user_ans not in ['A','B','C','D']:
            points = 3
        else:
            points = q['scores'].get(user_ans, 3)
        
        total_points += points
        total_questions += 1
        
        dim = q.get('dimension', 'unknown')
        dim_sums[dim] = dim_sums.get(dim, 0) + points
        dim_counts[dim] = dim_counts.get(dim, 0) + 1
    
    min_possible = total_questions * 1
    max_possible = total_questions * 5
    if max_possible == min_possible:
        raw_0_100 = 50
    else:
        raw_0_100 = ((total_points - min_possible) / (max_possible - min_possible)) * 100
        raw_0_100 = max(0, min(100, raw_0_100))
    
    sub_scores = {}
    for dim, sum_pts in dim_sums.items():
        count = dim_counts[dim]
        avg = sum_pts / count
        sub = ((avg - 1) / 4) * 100
        sub = max(0, min(100, sub))
        sub_scores[dim] = int(round(sub))
    
    return {
        "raw_score": int(round(raw_0_100)),
        "raw_points": total_points,
        "sub_scores": sub_scores,
        "adjusted_score": None
    }

# ---------- Master scorer ----------
def score_all(all_answers, age):
    """
    Main scoring function called from main.py.
    all_answers: dict like {'IQ': {qid: answer}, 'EQ': {...}, ...}
    age: int

    Returns: dict like
    {
        'IQ': {'adjusted_score': 108, 'raw_score': 22, ...},
        'EQ': {'adjusted_score': 74, 'raw_score': 42, 'sub_scores': {...}},
        ...
    }
    """
    results = {}
    
    # IQ
    if 'IQ' in all_answers and IQ_QUESTIONS:
        iq_data = score_iq(all_answers['IQ'], IQ_QUESTIONS)
        adjusted = compute_adjusted_score(iq_data['raw_percent'], age, 'IQ')
        results['IQ'] = {
            'adjusted_score': adjusted,
            'raw_score': iq_data['raw_score']
        }
    
    # EQ
    if 'EQ' in all_answers and EQ_QUESTIONS:
        eq_data = score_eq(all_answers['EQ'], EQ_QUESTIONS)
        adjusted = compute_adjusted_score(eq_data['raw_score'], age, 'EQ')
        results['EQ'] = {
            'adjusted_score': adjusted,
            'raw_score': eq_data['raw_score'],
            'sub_scores': eq_data['sub_scores']
        }
    
    # SQ
    if 'SQ' in all_answers and SQ_QUESTIONS:
        sq_data = score_sq(all_answers['SQ'], SQ_QUESTIONS)
        adjusted = compute_adjusted_score(sq_data['raw_score'], age, 'SQ')
        results['SQ'] = {
            'adjusted_score': adjusted,
            'raw_score': sq_data['raw_score'],
            'sub_scores': sq_data['sub_scores']
        }
    
    # AQ
    if 'AQ' in all_answers and AQ_QUESTIONS:
        aq_data = score_aq(all_answers['AQ'], AQ_QUESTIONS)
        adjusted = compute_adjusted_score(aq_data['raw_score'], age, 'AQ')
        results['AQ'] = {
            'adjusted_score': adjusted,
            'raw_score': aq_data['raw_score'],
            'sub_scores': aq_data['sub_scores']
        }
    
    return results