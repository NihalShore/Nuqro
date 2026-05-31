#!/usr/bin/env python3
"""
Unit tests for scorer.py – checks scoring calculations and norm application.
"""

import unittest
import sys
import os
import json
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock the NORMS_FILE to avoid cluttering real data
from nuqro import scorer
from nuqro.scorer import (
    score_iq, score_eq, score_sq, score_aq,
    compute_adjusted_score, load_norms, get_age_group
)
from nuqro.questions import IQ_QUESTIONS, EQ_QUESTIONS, SQ_QUESTIONS, AQ_QUESTIONS

class TestScorer(unittest.TestCase):
    
    def setUp(self):
        # Use a temporary directory for norms file during tests
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_norms_file = scorer.NORMS_FILE
        scorer.NORMS_FILE = Path(self.temp_dir.name) / "norms.json"
    
    def tearDown(self):
        scorer.NORMS_FILE = self.original_norms_file
        self.temp_dir.cleanup()
    
    def test_score_iq_perfect(self):
        answers = {}
        for q in IQ_QUESTIONS[:5]:  # test only first 5
            answers[q['id']] = q['correct']
        result = score_iq(answers, IQ_QUESTIONS[:5])
        self.assertEqual(result['raw_score'], 5)
        self.assertAlmostEqual(result['raw_percent'], 100.0)
    
    def test_score_iq_wrong(self):
        answers = {}
        for q in IQ_QUESTIONS[:5]:
            # give wrong answer (always A, but correct may not be A)
            answers[q['id']] = 'A'
        result = score_iq(answers, IQ_QUESTIONS[:5])
        # Count how many correct answers are 'A'
        expected_correct = sum(1 for q in IQ_QUESTIONS[:5] if q['correct'] == 'A')
        self.assertEqual(result['raw_score'], expected_correct)
    
    def test_score_eq(self):
        # Simulate perfect answers (all 'D' which should have highest score)
        # We need to know which answer gives max score (usually 5)
        # For simplicity, we'll look at the first EQ question's scores.
        if not EQ_QUESTIONS:
            self.skipTest("No EQ questions")
        # Find answer with max score for first question
        first_q = EQ_QUESTIONS[0]
        max_letter = max(first_q['scores'], key=lambda l: first_q['scores'][l])
        answers = {first_q['id']: max_letter}
        result = score_eq(answers, [first_q])
        # Raw score should be 100 (since one question max)
        self.assertEqual(result['raw_score'], 100)
        self.assertIn('sub_scores', result)
    
    def test_score_eq_missing_answer(self):
        # Missing answer should default to 3 (neutral)
        if not EQ_QUESTIONS:
            self.skipTest("No EQ questions")
        first_q = EQ_QUESTIONS[0]
        answers = {}  # no answer
        result = score_eq(answers, [first_q])
        # Neutral (3) maps to raw score: ((3-1)/4)*100 = 50
        self.assertEqual(result['raw_score'], 50)
    
    def test_compute_adjusted_score(self):
        # For IQ: raw 100 should give adjusted around 100+? depends on norm.
        # But we can test that function returns an integer.
        adj = compute_adjusted_score(100, 25, 'IQ')
        self.assertIsInstance(adj, int)
        # For EQ/SQ/AQ, clamped 0-100
        adj = compute_adjusted_score(100, 25, 'EQ')
        self.assertBetween(adj, 0, 100)
    
    def assertBetween(self, val, low, high):
        self.assertTrue(low <= val <= high, f"{val} not between {low} and {high}")
    
    def test_get_age_group(self):
        norms = load_norms()
        # Test boundaries
        self.assertEqual(get_age_group(10, norms, 'IQ'), '10-12')
        self.assertEqual(get_age_group(12, norms, 'IQ'), '10-12')
        self.assertEqual(get_age_group(13, norms, 'IQ'), '13-15')
        self.assertEqual(get_age_group(25, norms, 'IQ'), '19-25')
        self.assertEqual(get_age_group(51, norms, 'IQ'), '51+')
        self.assertEqual(get_age_group(80, norms, 'IQ'), '51+')
    
    def test_norms_file_created(self):
        # Remove any existing norms in temp dir
        if scorer.NORMS_FILE.exists():
            scorer.NORMS_FILE.unlink()
        norms = load_norms()
        self.assertTrue(scorer.NORMS_FILE.exists())
        self.assertIn('IQ', norms)
        self.assertIn('EQ', norms)

if __name__ == '__main__':
    unittest.main()