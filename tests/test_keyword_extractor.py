import sys
import os
import unittest

# Add the parent directory (project root) to sys.path to resolve imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.keyword_extractor import (
    extract_keywords_tfidf,
    extract_noun_chunks_spacy
)

class TestKeywordExtractor(unittest.TestCase):
    def test_extract_keywords_tfidf(self):
        """Test that TF-IDF keyword extraction works correctly."""
        # Test with a simple corpus
        corpus = [
            "Python is a programming language with many libraries for data science.",
            "Data science involves statistics, machine learning, and programming.",
            "Machine learning algorithms can be implemented in Python."
        ]
        
        # Extract keywords
        keywords_lists = extract_keywords_tfidf(corpus, top_n=3)
        
        # Check that the result is a list of lists
        self.assertIsInstance(keywords_lists, list)
        self.assertEqual(len(keywords_lists), len(corpus))
        
        # Check that each inner list contains strings
        for keywords in keywords_lists:
            self.assertIsInstance(keywords, list)
            for keyword in keywords:
                self.assertIsInstance(keyword, str)
        
        # Test with empty corpus
        empty_result = extract_keywords_tfidf([])
        self.assertEqual(empty_result, [])
        
        # Test with corpus containing empty string
        empty_string_result = extract_keywords_tfidf([""])
        self.assertEqual(empty_string_result, [[]])
        
        # Test with non-string input
        non_string_result = extract_keywords_tfidf([123])
        self.assertEqual(non_string_result, [[]])
    
    def test_extract_noun_chunks_spacy(self):
        """Test that noun chunk extraction works correctly."""
        # This test depends on spaCy being available
        # If spaCy is not available, the function should return an empty list
        
        # Test with a simple text
        text = "Python is a programming language with many libraries for data science."
        result = extract_noun_chunks_spacy(text)
        
        # The result should be a list
        self.assertIsInstance(result, list)
        
        # If spaCy is available, the result should contain noun chunks
        # Common noun chunks in the text: "Python", "a programming language", "many libraries", "data science"
        # But we can't assert exact matches as spaCy's behavior might vary
        
        # Test with empty string
        empty_result = extract_noun_chunks_spacy("")
        self.assertEqual(empty_result, [])
        
        # Test with non-string input
        non_string_result = extract_noun_chunks_spacy(123)
        self.assertEqual(non_string_result, [])

if __name__ == '__main__':
    unittest.main()
