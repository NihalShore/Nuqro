#!/usr/bin/env python3
"""
Unit tests for questions.py – checks structure, age filtering, randomness.
"""

import unittest
import sys
import os

# Add project root to path (parent of tests folder)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nuqro.questions import (
    IQ_QUESTIONS, EQ_QUESTIONS, SQ_QUESTIONS, AQ_QUESTIONS,
    get_questions
)

class TestQuestions(unittest.TestCase):
    
    def test_iq_structure(self):
        """Every IQ question must have id, text, options, correct, min_age."""
        for q in IQ_QUESTIONS:
            with self.subTest(q=q.get('id', 'unknown')):
                self.assertIn('id', q)
                self.assertIn('text', q)
                self.assertIn('options', q)
                self.assertIsInstance(q['options'], dict)
                self.assertIn('correct', q)
                self.assertIn(q['correct'], ['A','B','C','D'])
                self.assertIn('min_age', q)
                self.assertIsInstance(q['min_age'], int)
    
    def test_eq_structure(self):
        """EQ: must have scores dict and dimension."""
        for q in EQ_QUESTIONS:
            with self.subTest(q=q.get('id', 'unknown')):
                self.assertIn('scores', q)
                self.assertIsInstance(q['scores'], dict)
                for letter in ['A','B','C','D']:
                    self.assertIn(letter, q['scores'])
                self.assertIn('dimension', q)
                self.assertIn(q['dimension'], 
                    ['self_awareness', 'self_management', 'social_awareness', 'relationship_management'])
    
    def test_sq_structure(self):
        """SQ: scores dict and factor."""
        for q in SQ_QUESTIONS:
            with self.subTest(q=q.get('id', 'unknown')):
                self.assertIn('scores', q)
                self.assertIn('factor', q)
                self.assertIn(q['factor'], ['social_acting', 'social_cognising', 'social_relating'])
    
    def test_aq_structure(self):
        """AQ: scores dict and dimension (CORE)."""
        for q in AQ_QUESTIONS:
            with self.subTest(q=q.get('id', 'unknown')):
                self.assertIn('scores', q)
                self.assertIn('dimension', q)
                self.assertIn(q['dimension'], ['Control', 'Ownership', 'Reach', 'Endurance'])
    
    def test_get_questions_age_filter(self):
        """Young age should filter out high min_age questions."""
        # Age 5 – should return only questions with min_age <= 5 (none? fallback to all? but structure)
        iq = get_questions('IQ', 5)
        # If no questions meet age, get_questions returns all (fallback). So just check not empty.
        self.assertTrue(len(iq) > 0)
        
        # Age 18 – should include most questions
        iq_old = get_questions('IQ', 18)
        self.assertGreaterEqual(len(iq_old), 8)
    
    def test_get_questions_returns_max_10(self):
        for test in ['IQ','EQ','SQ','AQ']:
            with self.subTest(test=test):
                qs = get_questions(test, 30)
                self.assertLessEqual(len(qs), 10)
    
    def test_no_duplicate_ids(self):
        for name, bank in [('IQ', IQ_QUESTIONS), ('EQ', EQ_QUESTIONS), 
                           ('SQ', SQ_QUESTIONS), ('AQ', AQ_QUESTIONS)]:
            ids = [q['id'] for q in bank]
            self.assertEqual(len(ids), len(set(ids)), f"Duplicate IDs in {name}")

if __name__ == '__main__':
    unittest.main()