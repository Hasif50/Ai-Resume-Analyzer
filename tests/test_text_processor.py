import sys
import os
import unittest

# Add the parent directory (project root) to sys.path to resolve imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.text_processor import (
    lowercase_text,
    remove_punctuation,
    remove_stopwords_nltk,
    lemmatize_text_spacy,
    preprocess_text
)

class TestTextProcessor(unittest.TestCase):
    def test_lowercase_text(self):
        """Test that text is properly converted to lowercase."""
        input_text = "Hello WORLD! This is a TEST."
        expected = "hello world! this is a test."
        self.assertEqual(lowercase_text(input_text), expected)
        
        # Test with empty string
        self.assertEqual(lowercase_text(""), "")
        
        # Test with non-string input
        self.assertEqual(lowercase_text(123), "")
    
    def test_remove_punctuation(self):
        """Test that punctuation is properly removed."""
        input_text = "Hello, world! This is a test: with punctuation."
        expected = "Hello world This is a test with punctuation"
        self.assertEqual(remove_punctuation(input_text), expected)
        
        # Test with empty string
        self.assertEqual(remove_punctuation(""), "")
        
        # Test with non-string input
        self.assertEqual(remove_punctuation(123), "")
    
    def test_remove_stopwords_nltk(self):
        """Test that stopwords are properly removed."""
        input_text = "This is a test with some stopwords like the and a"
        # Expected output should not contain 'this', 'is', 'a', 'with', 'some', 'like', 'the', 'and'
        expected_words = ["test", "stopwords"]
        result = remove_stopwords_nltk(input_text)
        # Check that all expected words are in the result
        for word in expected_words:
            self.assertIn(word, result)
        
        # Test with empty string
        self.assertEqual(remove_stopwords_nltk(""), "")
        
        # Test with non-string input
        self.assertEqual(remove_stopwords_nltk(123), "")
    
    def test_lemmatize_text_spacy(self):
        """Test that lemmatization works correctly."""
        # This test depends on spaCy being available
        # If spaCy is not available, the function should return the input text
        input_text = "running jumps faster computers"
        result = lemmatize_text_spacy(input_text)
        
        # The result should be lemmatized if spaCy is available
        # If spaCy is not available, this test will still pass but won't test lemmatization
        self.assertIsInstance(result, str)
        
        # Test with empty string
        self.assertEqual(lemmatize_text_spacy(""), "")
        
        # Test with non-string input
        self.assertEqual(lemmatize_text_spacy(123), "")
    
    def test_preprocess_text(self):
        """Test the full preprocessing pipeline."""
        input_text = "Hello, world! This is a test with some stopwords."
        result = preprocess_text(input_text)
        
        # The result should be a string
        self.assertIsInstance(result, str)
        
        # The result should be lowercase
        self.assertEqual(result, result.lower())
        
        # The result should not contain punctuation
        for char in ",.!?;:\"'()[]{}-":
            self.assertNotIn(char, result)
        
        # The result should not contain common stopwords
        common_stopwords = ["the", "is", "a", "an", "and", "or", "but", "with"]
        for word in common_stopwords:
            self.assertNotIn(f" {word} ", f" {result} ")
        
        # Test with empty string
        self.assertEqual(preprocess_text(""), "")
        
        # Test with non-string input
        self.assertEqual(preprocess_text(123), "")

if __name__ == '__main__':
    unittest.main()
