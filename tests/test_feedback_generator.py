import sys
import os
import unittest

# Add the parent directory (project root) to sys.path to resolve imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.feedback_generator import generate_feedback

class TestFeedbackGenerator(unittest.TestCase):
    def test_generate_feedback_high_score(self):
        """Test feedback generation for high scores."""
        resume_keywords = ["python", "django", "api", "web development", "machine learning"]
        jd_keywords = ["python", "django", "api", "restful services", "machine learning"]
        semantic_similarity_score = 0.85
        overall_score = 88.0
        
        feedback = generate_feedback(
            resume_keywords, jd_keywords, semantic_similarity_score, overall_score
        )
        
        # Check that the feedback is a dictionary
        self.assertIsInstance(feedback, dict)
        
        # Check that the feedback contains the expected keys
        self.assertIn('overall_summary', feedback)
        self.assertIn('strengths', feedback)
        
        # For high scores, there should be a positive overall summary
        self.assertTrue(any("excellent" in summary.lower() for summary in feedback['overall_summary']))
        
        # For high semantic similarity, there should be a strength about semantic alignment
        self.assertTrue(any("semantic" in strength.lower() for strength in feedback['strengths']))
    
    def test_generate_feedback_medium_score(self):
        """Test feedback generation for medium scores."""
        resume_keywords = ["java", "spring boot", "sql", "backend development"]
        jd_keywords = ["java", "spring", "microservices", "api design", "cloud", "kubernetes"]
        semantic_similarity_score = 0.60
        overall_score = 55.0
        
        feedback = generate_feedback(
            resume_keywords, jd_keywords, semantic_similarity_score, overall_score
        )
        
        # Check that the feedback is a dictionary
        self.assertIsInstance(feedback, dict)
        
        # Check that the feedback contains the expected keys
        self.assertIn('overall_summary', feedback)
        
        # For medium scores, there should be a neutral overall summary
        self.assertTrue(any("good potential" in summary.lower() for summary in feedback['overall_summary']))
        
        # There should be missing keywords suggestions
        self.assertIn('missing_keywords_suggestions', feedback)
        
        # Check that missing keywords are suggested
        missing_keywords = set(jd_keywords) - set(resume_keywords)
        missing_keywords_text = ' '.join(feedback['missing_keywords_suggestions']).lower()
        for keyword in missing_keywords:
            if keyword in ['microservices', 'api design', 'cloud', 'kubernetes']:
                # These are the keywords that should be missing
                # We don't check for exact matches, just that they're mentioned somewhere
                self.assertTrue(
                    keyword.lower() in missing_keywords_text,
                    f"Missing keyword '{keyword}' not mentioned in suggestions"
                )
    
    def test_generate_feedback_low_score(self):
        """Test feedback generation for low scores."""
        resume_keywords = ["marketing", "social media", "content creation"]
        jd_keywords = ["software engineer", "c++", "systems programming", "algorithms"]
        semantic_similarity_score = 0.20
        overall_score = 15.0
        
        feedback = generate_feedback(
            resume_keywords, jd_keywords, semantic_similarity_score, overall_score
        )
        
        # Check that the feedback is a dictionary
        self.assertIsInstance(feedback, dict)
        
        # Check that the feedback contains the expected keys
        self.assertIn('overall_summary', feedback)
        
        # For low scores, there should be a negative overall summary
        self.assertTrue(any("needs improvement" in summary.lower() for summary in feedback['overall_summary']))
        
        # There should be areas for improvement
        self.assertIn('areas_for_improvement', feedback)
        
        # For low semantic similarity, there should be a suggestion about improving semantic relevance
        self.assertTrue(any("semantic" in improvement.lower() for improvement in feedback['areas_for_improvement']))
    
    def test_generate_feedback_missing_keywords(self):
        """Test feedback generation for missing keywords."""
        resume_keywords = ["python", "api", "web development"]
        jd_keywords = ["python", "django", "api", "machine learning", "web development"]
        semantic_similarity_score = 0.75
        overall_score = 70.0
        
        feedback = generate_feedback(
            resume_keywords, jd_keywords, semantic_similarity_score, overall_score, top_n_missing_keywords=2
        )
        
        # Check that the feedback is a dictionary
        self.assertIsInstance(feedback, dict)
        
        # There should be missing keywords suggestions
        self.assertIn('missing_keywords_suggestions', feedback)
        
        # Check that missing keywords are suggested
        missing_keywords = set(jd_keywords) - set(resume_keywords)
        missing_keywords_text = ' '.join(feedback['missing_keywords_suggestions']).lower()
        for keyword in missing_keywords:
            if keyword in ['django', 'machine learning']:
                # These are the keywords that should be missing
                # We don't check for exact matches, just that they're mentioned somewhere
                self.assertTrue(
                    keyword.lower() in missing_keywords_text,
                    f"Missing keyword '{keyword}' not mentioned in suggestions"
                )

if __name__ == '__main__':
    unittest.main()
