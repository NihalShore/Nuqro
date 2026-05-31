#!/usr/bin/env python3
"""
Integration tests: runs a full simulated test session from questions to scoring.
"""

import unittest
import sys
import os
import tempfile
import shutil
import io
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from nuqro.questions import get_questions
from nuqro.scorer import score_all
from nuqro.report import print_full_report, export_report

class TestIntegration(unittest.TestCase):
    
    def setUp(self):
        # Capture print output
        self.captured = io.StringIO()
        self.old_stdout = sys.stdout
        sys.stdout = self.captured
        
        # Create temporary directories for reports and data
        self.temp_reports = tempfile.mkdtemp()
        self.temp_data = tempfile.mkdtemp()
        
        # Override report's reports directory (hack: monkey-patch the export function's path?)
        # Simpler: change working directory? No, we can just let report write to its default
        # and then clean up after. But to avoid interfering with real project, we patch the Path.
        # Instead, we'll temporarily rename the existing reports folder if any.
        self.original_reports = Path("reports")
        self.original_data = Path("data")
        if self.original_reports.exists():
            self.original_reports.rename(self.original_reports.with_suffix(".backup"))
        if self.original_data.exists():
            self.original_data.rename(self.original_data.with_suffix(".backup"))
        
        # Create fresh empty directories for test
        self.original_reports.mkdir(exist_ok=True)
        self.original_data.mkdir(exist_ok=True)
    
    def tearDown(self):
        sys.stdout = self.old_stdout
        
        # Clean up test directories
        shutil.rmtree(self.temp_reports, ignore_errors=True)
        shutil.rmtree(self.temp_data, ignore_errors=True)
        
        # Restore original directories
        if self.original_reports.with_suffix(".backup").exists():
            shutil.rmtree(self.original_reports, ignore_errors=True)
            self.original_reports.with_suffix(".backup").rename(self.original_reports)
        else:
            shutil.rmtree(self.original_reports, ignore_errors=True)
        
        if self.original_data.with_suffix(".backup").exists():
            shutil.rmtree(self.original_data, ignore_errors=True)
            self.original_data.with_suffix(".backup").rename(self.original_data)
        else:
            shutil.rmtree(self.original_data, ignore_errors=True)
    
    def test_full_pipeline_no_crash(self):
        age = 25
        all_answers = {}
        for test in ['IQ', 'EQ', 'SQ', 'AQ']:
            questions = get_questions(test, age)
            answers = {q['id']: 'A' for q in questions}  # always 'A'
            all_answers[test] = answers
        
        results = score_all(all_answers, age)
        
        for test in ['IQ', 'EQ', 'SQ', 'AQ']:
            self.assertIn(test, results)
            self.assertIn('adjusted_score', results[test])
            self.assertIn('raw_score', results[test])
            if test != 'IQ':
                self.assertIn('sub_scores', results[test])
        
        # Print report
        print_full_report("TestUser", age, results)
        output = self.captured.getvalue()
        self.assertIn("NUQRO REPORT", output)
        self.assertIn("TestUser", output)
        
        # Export
        export_report("TestUser", age, results, format='txt')
        export_report("TestUser", age, results, format='json')
        
        # Check files were created
        reports_dir = Path("reports")
        self.assertTrue(reports_dir.exists())
        txt_files = list(reports_dir.glob("*.txt"))
        json_files = list(reports_dir.glob("*.json"))
        self.assertGreaterEqual(len(txt_files), 1)
        self.assertGreaterEqual(len(json_files), 1)
    
    def test_resume_data_integration(self):
        age = 30
        questions = get_questions('EQ', age)
        answers = {}
        for i, q in enumerate(questions):
            if i < len(questions) // 2:
                answers[q['id']] = 'B'
        all_answers = {'EQ': answers}
        results = score_all(all_answers, age)
        self.assertIn('EQ', results)
        self.assertIsNotNone(results['EQ']['adjusted_score'])

if __name__ == '__main__':
    unittest.main()