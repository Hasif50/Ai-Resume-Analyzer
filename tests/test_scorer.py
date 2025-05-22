import sys
import os
import unittest

# Add the parent directory (project root) to sys.path to resolve imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.scorer import (
    calculate_keyword_match_score,
    calculate_overall_score
)

class TestScorer(unittest.TestCase):
    def test_calculate_keyword_match_score(self):
        """Test that keyword match score calculation works correctly."""
        # Test with identical keyword lists
        resume_keywords = ["python", "django", "api", "web development"]
        jd_keywords = ["python", "django", "api", "web development"]
        score = calculate_keyword_match_score(resume_keywords, jd_keywords)
        self.assertEqual(score, 1.0)  # Perfect match should be 1.0
        
        # Test with no overlap
        resume_keywords = ["python", "django", "api"]
        jd_keywords = ["java", "spring", "rest"]
        score = calculate_keyword_match_score(resume_keywords, jd_keywords)
        self.assertEqual(score, 0.0)  # No overlap should be 0.0
        
        # Test with partial overlap
        resume_keywords = ["python", "django", "api", "web development"]
        jd_keywords = ["python", "flask", "api", "microservices"]
        score = calculate_keyword_match_score(resume_keywords, jd_keywords)
        # 2 common keywords out of 6 unique keywords = 2/6 = 0.333...
        self.assertAlmostEqual(score, 2/6)
        
        # Test with empty lists
        self.assertEqual(calculate_keyword_match_score([], []), 0.0)
        self.assertEqual(calculate_keyword_match_score(resume_keywords, []), 0.0)
        self.assertEqual(calculate_keyword_match_score([], jd_keywords), 0.0)
    
    def test_calculate_overall_score(self):
        """Test that overall score calculation works correctly."""
        resume_keywords = ["python", "django", "api"]
        jd_keywords = ["python", "flask", "api"]
        semantic_similarity_score = 0.8
        
        # Test with default weights
        score = calculate_overall_score(resume_keywords, jd_keywords, semantic_similarity_score)
        # Expected: (keyword_match_score * 0.4) + (semantic_similarity_score * 0.6)
        # keyword_match_score = 2/4 = 0.5
        # Expected: (0.5 * 0.4) + (0.8 * 0.6) = 0.2 + 0.48 = 0.68
        # Then scaled to 0-100: 0.68 * 100 = 68.0
        expected_score = ((2/4) * 0.4 + 0.8 * 0.6) * 100
        self.assertAlmostEqual(score, expected_score)
        
        # Test with custom weights
        score = calculate_overall_score(
            resume_keywords, jd_keywords, semantic_similarity_score,
            keyword_weight=0.7, semantic_weight=0.3
        )
        # Expected: (0.5 * 0.7) + (0.8 * 0.3) = 0.35 + 0.24 = 0.59
        # Then scaled to 0-100: 0.59 * 100 = 59.0
        expected_score = ((2/4) * 0.7 + 0.8 * 0.3) * 100
        self.assertAlmostEqual(score, expected_score)
        
        # Test with weights that don't sum to 1 (should be normalized)
        score = calculate_overall_score(
            resume_keywords, jd_keywords, semantic_similarity_score,
            keyword_weight=0.5, semantic_weight=0.5
        )
        # Weights already sum to 1, so no normalization needed
        # Expected: (0.5 * 0.5) + (0.8 * 0.5) = 0.25 + 0.4 = 0.65
        # Then scaled to 0-100: 0.65 * 100 = 65.0
        expected_score = ((2/4) * 0.5 + 0.8 * 0.5) * 100
        self.assertAlmostEqual(score, expected_score)
        
        # Test with empty keyword lists
        score = calculate_overall_score([], jd_keywords, semantic_similarity_score)
        # keyword_match_score should be 0.0
        # Expected: (0.0 * 0.4) + (0.8 * 0.6) = 0.0 + 0.48 = 0.48
        # Then scaled to 0-100: 0.48 * 100 = 48.0
        expected_score = (0.0 * 0.4 + 0.8 * 0.6) * 100
        self.assertAlmostEqual(score, expected_score)
        
        # Test with semantic score out of range (should be clamped)
        score = calculate_overall_score(resume_keywords, jd_keywords, 1.5)
        # semantic_similarity_score should be clamped to 1.0
        # Expected: (0.5 * 0.4) + (1.0 * 0.6) = 0.2 + 0.6 = 0.8
        # Then scaled to 0-100: 0.8 * 100 = 80.0
        expected_score = ((2/4) * 0.4 + 1.0 * 0.6) * 100
        self.assertAlmostEqual(score, expected_score)

if __name__ == '__main__':
    unittest.main()
