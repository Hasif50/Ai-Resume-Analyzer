import sys
import os

# Add the parent directory (project root) to sys.path to resolve imports like 'from backend.module'
# This needs to be done before attempting to import from 'backend'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from backend.text_processor import preprocess_text  # For example usage

# Load a pre-trained Sentence Transformer model
# This is done once when the module is loaded.
MODEL_NAME = 'all-MiniLM-L6-v2'
try:
    sentence_model = SentenceTransformer(MODEL_NAME)
    print(f"Sentence Transformer model '{MODEL_NAME}' loaded successfully.")
except Exception as e:
    print(f"Error loading Sentence Transformer model '{MODEL_NAME}': {e}")
    print("Semantic similarity functions may not work as expected.")
    sentence_model = None

def calculate_semantic_similarity(text1, text2):
    """
    Calculates the semantic similarity between two texts using Sentence Transformers.
    
    Args:
        text1 (str): The first text string.
        text2 (str): The second text string.
    
    Returns:
        float: The cosine similarity score between the two texts (between 0 and 1).
               Returns 0.0 if an error occurs or the model is not loaded.
    """
    if sentence_model is None:
        print("Error: Sentence Transformer model is not loaded. Cannot calculate similarity.")
        return 0.0
    
    if not isinstance(text1, str) or not isinstance(text2, str):
        print("Error: Both inputs must be strings.")
        return 0.0
    
    if not text1.strip() or not text2.strip():
        # Handle empty or whitespace-only strings
        # print("Warning: One or both input texts are empty/whitespace. Similarity will be low or undefined.")
        # Embeddings of empty strings can be problematic or lead to NaN if not handled.
        # SentenceTransformer might handle this, but good to be aware.
        # If one is empty and other is not, similarity should ideally be 0.
        # If both are empty, it's undefined, could be 1 or 0 depending on implementation.
        # For simplicity, if either is effectively empty, we can return 0.
        if not text1.strip() and not text2.strip():
            # Both are empty
            return 1.0  # Or 0.0, debatable. Let's say two empty strings are perfectly similar.
        return 0.0
    
    try:
        embeddings = sentence_model.encode([text1, text2])
        # Reshape for cosine_similarity: it expects 2D arrays
        similarity_score = cosine_similarity(embeddings[0].reshape(1, -1), embeddings[1].reshape(1, -1))[0][0]
        return float(similarity_score)  # Ensure it's a standard float
    
    except Exception as e:
        print(f"Error during semantic similarity calculation: {e}")
        return 0.0

if __name__ == '__main__':
    if sentence_model is None:
        print("\nSkipping semantic similarity examples as the model could not be loaded.")
    else:
        print("\n### Testing Semantic Similarity Calculation ###")
        print("-" * 40)
        
        resume_snippet = "Experienced Python developer with skills in web development, Django, and REST APIs."
        job_description_1 = "Seeking a Senior Python Engineer for backend development using Django and microservices."
        job_description_2 = "Looking for a front-end developer with React and JavaScript expertise."
        job_description_3 = "Experienced Python developer with skills in web development, Django, and REST APIs."  # Identical to resume
        empty_text = ""
        whitespace_text = " "
        
        print(f"Resume: \"{resume_snippet}\"")
        print(f"Job Desc 1: \"{job_description_1}\"")
        print(f"Job Desc 2: \"{job_description_2}\"")
        print(f"Job Desc 3 (Identical): \"{job_description_3}\"")
        print("-" * 40)
        
        # --- Test 1: Resume vs Job Description 1 (should be high similarity) ---
        similarity_1 = calculate_semantic_similarity(resume_snippet, job_description_1)
        print(f"Similarity (Resume vs Job 1): {similarity_1:.4f}")
        
        # --- Test 2: Resume vs Job Description 2 (should be low similarity) ---
        similarity_2 = calculate_semantic_similarity(resume_snippet, job_description_2)
        print(f"Similarity (Resume vs Job 2): {similarity_2:.4f}")
        
        # --- Test 3: Identical texts ---
        similarity_3 = calculate_semantic_similarity(resume_snippet, resume_snippet)
        print(f"Similarity (Identical texts - resume vs resume): {similarity_3:.4f}")
        
        similarity_identical_jd = calculate_semantic_similarity(resume_snippet, job_description_3)
        print(f"Similarity (Identical texts - resume vs job_description_3): {similarity_identical_jd:.4f}")
        
        # --- Test 4: Impact of preprocessing ---
        print("\n--- Testing with Preprocessing ---")
        processed_resume = preprocess_text(resume_snippet)
        processed_jd1 = preprocess_text(job_description_1)
        processed_jd2 = preprocess_text(job_description_2)
        
        print(f"Processed Resume: \"{processed_resume}\"")
        print(f"Processed Job Desc 1: \"{processed_jd1}\"")
        
        similarity_processed_1 = calculate_semantic_similarity(processed_resume, processed_jd1)
        print(f"Similarity (Processed Resume vs Processed Job 1): {similarity_processed_1:.4f}")
        
        # For sentence transformers, preprocessing like stopword removal or lemmatization
        # might sometimes hurt performance as they are trained on natural language.
        # However, it can also sometimes help by removing noise. Worth testing.
        
        # --- Test 5: Edge cases (empty strings) ---
        print("\n--- Testing Edge Cases ---")
        similarity_empty_both = calculate_semantic_similarity(empty_text, empty_text)
        print(f"Similarity (Empty vs Empty): {similarity_empty_both:.4f}")
        
        similarity_empty_one = calculate_semantic_similarity(resume_snippet, empty_text)
        print(f"Similarity (Resume vs Empty): {similarity_empty_one:.4f}")
        
        similarity_whitespace_both = calculate_semantic_similarity(whitespace_text, whitespace_text)
        print(f"Similarity (Whitespace vs Whitespace): {similarity_whitespace_both:.4f}")
        
        similarity_whitespace_one = calculate_semantic_similarity(resume_snippet, whitespace_text)
        print(f"Similarity (Resume vs Whitespace): {similarity_whitespace_one:.4f}")
        
        print("-" * 40)
