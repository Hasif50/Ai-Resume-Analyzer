import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    print("Testing text_processor module...")
    from backend.text_processor import preprocess_text
    print("preprocess_text imported successfully")
    
    print("\nTesting keyword_extractor module...")
    from backend.keyword_extractor import extract_keywords_tfidf
    print("extract_keywords_tfidf imported successfully")
    
    print("\nTesting semantic_analyzer module...")
    from backend.semantic_analyzer import calculate_semantic_similarity, sentence_model
    print(f"calculate_semantic_similarity imported successfully")
    print(f"sentence_model loaded: {sentence_model is not None}")
    
    print("\nTesting scorer module...")
    from backend.scorer import calculate_overall_score, calculate_keyword_match_score
    print("scorer functions imported successfully")
    
    print("\nTesting feedback_generator module...")
    from backend.feedback_generator import generate_feedback
    print("generate_feedback imported successfully")
    
    print("\nAll modules imported successfully!")
    
    # Test a simple preprocessing
    sample_text = "This is a test sentence for preprocessing."
    processed_text = preprocess_text(sample_text)
    print(f"\nSample text: '{sample_text}'")
    print(f"Processed text: '{processed_text}'")
    
    # Test keyword extraction
    keywords = extract_keywords_tfidf([processed_text])
    print(f"\nExtracted keywords: {keywords}")
    
    # Test semantic similarity
    text1 = "Python developer with experience in web development"
    text2 = "Looking for a software engineer with Python skills"
    similarity = calculate_semantic_similarity(text1, text2)
    print(f"\nSemantic similarity between '{text1}' and '{text2}': {similarity:.4f}")
    
    print("\nAll tests completed successfully!")
    
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
