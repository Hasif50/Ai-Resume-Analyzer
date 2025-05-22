import sys
import os

# Add the parent directory (project root) to sys.path to resolve imports like 'from backend.module'
# This needs to be done before attempting to import from 'backend'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from backend.text_processor import preprocess_text

# Load spaCy model
# This should have been downloaded during the setup phase (python -m spacy download en_core_web_sm)
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print("SpaCy 'en_core_web_sm' model not found. Please run: python -m spacy download en_core_web_sm")
    nlp = None  # Set to None if essential and not found, functions should handle this

def extract_keywords_tfidf(processed_text_corpus, top_n=10):
    """
    Extracts keywords from a corpus of processed text documents using TF-IDF.
    
    Args:
        processed_text_corpus (list of str): A list of preprocessed text documents.
                                            For a single document, pass it as a list with one string.
        top_n (int): The number of top keywords to return for each document.
    
    Returns:
        list of list of str: A list of keyword lists, one for each document in the input corpus.
                            Returns an empty list if an error occurs or nlp model not found.
    """
    if not processed_text_corpus or not all(isinstance(doc, str) for doc in processed_text_corpus):
        print("Error: Input must be a non-empty list of strings.")
        return [[] for _ in processed_text_corpus] if processed_text_corpus else []
    
    try:
        vectorizer = TfidfVectorizer(stop_words='english')  # Use built-in stop words for TF-IDF
        tfidf_matrix = vectorizer.fit_transform(processed_text_corpus)
        feature_names = vectorizer.get_feature_names_out()
        
        corpus_keywords = []
        for i in range(tfidf_matrix.shape[0]):
            doc_vector = tfidf_matrix[i, :]
            # Get indices of features sorted by TF-IDF score in descending order
            sorted_indices = doc_vector.toarray().argsort()[0][::-1]
            
            doc_keywords = []
            for idx in sorted_indices[:top_n]:
                if doc_vector[0, idx] > 0:  # Ensure the keyword has a non-zero score
                    doc_keywords.append(feature_names[idx])
            
            corpus_keywords.append(doc_keywords)
        
        return corpus_keywords
    
    except Exception as e:
        print(f"Error during TF-IDF keyword extraction: {e}")
        return [[] for _ in processed_text_corpus] if processed_text_corpus else []

def extract_noun_chunks_spacy(text):
    """
    Extracts noun chunks from text using spaCy.
    Noun chunks are often good keyword candidates.
    
    Args:
        text (str): The input text (can be raw or partially processed).
    
    Returns:
        list of str: A list of noun chunks found in the text.
                    Returns an empty list if an error occurs or nlp model not found.
    """
    if not isinstance(text, str):
        print("Error: Input must be a string.")
        return []
    
    if nlp is None:
        print("SpaCy nlp model not loaded. Skipping noun chunk extraction.")
        return []
    
    try:
        doc = nlp(text)
        noun_chunks = [chunk.text for chunk in doc.noun_chunks]
        return noun_chunks
    
    except Exception as e:
        print(f"Error during spaCy noun chunk extraction: {e}")
        return []

if __name__ == '__main__':
    import sys
    import os
    # Add the parent directory (project root) to sys.path to resolve imports like 'from backend.module'
    
    sample_texts = [
        "Senior Python Developer with experience in web development, APIs, and Django.",
        "We are looking for a Data Scientist skilled in Machine Learning, Python, and data visualization.",
        "Another document about software engineering and cloud computing with AWS."
    ]
    
    single_text_example = "This is a simple example sentence about natural language processing and keyword spotting."
    
    print("### Testing Keyword Extraction ###")
    print("-" * 30)
    
    # --- Test with TF-IDF ---
    print("\n--- TF-IDF Keyword Extraction ---")
    
    # Preprocess the sample texts first
    processed_sample_texts = [preprocess_text(text) for text in sample_texts]
    print(f"Processed texts for TF-IDF: {processed_sample_texts}")
    
    if all(processed_sample_texts):  # Check if preprocessing returned non-empty strings
        keywords_tfidf_corpus = extract_keywords_tfidf(processed_sample_texts, top_n=5)
        for i, text in enumerate(sample_texts):
            print(f"\nOriginal: {text}")
            print(f"TF-IDF Keywords: {keywords_tfidf_corpus[i]}")
    else:
        print("\nSkipping TF-IDF on corpus due to preprocessing error or empty result.")
    
    # TF-IDF on a single document
    processed_single_text = preprocess_text(single_text_example)
    print(f"\nProcessed single text for TF-IDF: '{processed_single_text}'")
    
    if processed_single_text:
        keywords_tfidf_single = extract_keywords_tfidf([processed_single_text], top_n=5)  # Pass as a list
        print(f"\nOriginal: {single_text_example}")
        print(f"TF-IDF Keywords (single doc): {keywords_tfidf_single[0]}")  # Access the first element
    else:
        print("\nSkipping TF-IDF on single text due to preprocessing error or empty result.")
    
    print("-" * 30)
    
    # --- Test with spaCy Noun Chunks ---
    print("\n--- spaCy Noun Chunk Extraction ---")
    
    if nlp:
        for text in sample_texts:
            print(f"\nOriginal: {text}")
            noun_chunks = extract_noun_chunks_spacy(text)  # Use raw text for spaCy noun chunking usually
            print(f"SpaCy Noun Chunks: {noun_chunks}")
        
        print(f"\nOriginal (single text): {single_text_example}")
        noun_chunks_single = extract_noun_chunks_spacy(single_text_example)
        print(f"SpaCy Noun Chunks (single text): {noun_chunks_single}")
    else:
        print("\nSkipping spaCy Noun Chunk tests as 'en_core_web_sm' model is not loaded.")
    
    print("-" * 30)
    
    # Test edge cases
    empty_text_list = [""]
    processed_empty_text_list = [preprocess_text(t) for t in empty_text_list]
    print(f"\nTF-IDF with empty processed text list: {processed_empty_text_list}")
    tfidf_empty = extract_keywords_tfidf(processed_empty_text_list)
    print(f"TF-IDF Keywords (empty processed): {tfidf_empty}")
    
    print(f"\nSpaCy Noun Chunks with empty text: '{empty_text_list[0]}'")
    spacy_empty_chunks = extract_noun_chunks_spacy(empty_text_list[0])
    print(f"SpaCy Noun Chunks (empty): {spacy_empty_chunks}")
    
    print("-" * 30)
