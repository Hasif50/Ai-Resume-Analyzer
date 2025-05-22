import sys
import os

# Add the parent directory (project root) to sys.path to resolve imports like 'from backend.module'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Example inputs might come from these modules, so import for __main__ if needed
# from backend.text_processor import preprocess_text
# from backend.keyword_extractor import extract_keywords_tfidf, extract_noun_chunks_spacy
# from backend.semantic_analyzer import calculate_semantic_similarity

def calculate_keyword_match_score(resume_keywords, jd_keywords):
    """
    Calculates a score based on the overlap of keywords between resume and job description.
    Uses Jaccard similarity.
    
    Args:
        resume_keywords (list of str): A list of keywords extracted from the resume.
        jd_keywords (list of str): A list of keywords extracted from the job description.
    
    Returns:
        float: A score between 0 and 1 representing the keyword match.
               Returns 0.0 if either keyword list is empty.
    """
    if not resume_keywords or not jd_keywords:
        return 0.0
    
    set_resume = set(resume_keywords)
    set_jd = set(jd_keywords)
    
    intersection = len(set_resume.intersection(set_jd))
    union = len(set_resume.union(set_jd))
    
    if union == 0:
        return 0.0  # Should not happen if inputs are non-empty, but good for safety
    
    return intersection / union

def calculate_overall_score(resume_keywords, jd_keywords, semantic_similarity_score, keyword_weight=0.4, semantic_weight=0.6):
    """
    Calculates an overall score based on keyword matches and semantic similarity.
    
    The individual scores (keyword_match_score and semantic_similarity_score) are expected to be in the range [0, 1].
    The final score is scaled to be out of 100.
    
    Args:
        resume_keywords (list of str): Keywords extracted from the resume.
        jd_keywords (list of str): Keywords extracted from the job description.
        semantic_similarity_score (float): The semantic similarity score (0 to 1).
        keyword_weight (float): The weight assigned to the keyword match score.
        semantic_weight (float): The weight assigned to the semantic similarity score.
                                (keyword_weight + semantic_weight should ideally sum to 1)
    
    Returns:
        float: An overall score between 0 and 100.
    """
    if not (0 <= keyword_weight <= 1 and 0 <= semantic_weight <= 1):
        raise ValueError("Weights must be between 0 and 1.")
    
    if not (keyword_weight + semantic_weight > 0):  # Avoid division by zero if both are 0
        # Or ensure they sum to 1 for a weighted average interpretation
        print("Warning: Sum of weights is 0. Score will be 0.")
        return 0.0
    
    # Ensure weights sum to 1 for a true weighted average, or normalize them
    total_weight = keyword_weight + semantic_weight
    if total_weight != 1.0:
        print(f"Warning: Weights do not sum to 1. Normalizing weights for calculation. Original: kw={keyword_weight}, sw={semantic_weight}")
        if total_weight == 0:  # Should be caught above, but for safety
            return 0.0
        keyword_weight /= total_weight
        semantic_weight /= total_weight
    
    keyword_match_score = calculate_keyword_match_score(resume_keywords, jd_keywords)
    
    # Ensure semantic_similarity_score is within [0, 1]
    clamped_semantic_score = max(0.0, min(1.0, semantic_similarity_score))
    
    # Combine scores
    # The individual scores are already in [0,1]
    combined_score_0_to_1 = (keyword_match_score * keyword_weight) + \
                            (clamped_semantic_score * semantic_weight)
    
    overall_score_0_to_100 = combined_score_0_to_1 * 100
    
    return overall_score_0_to_100

if __name__ == '__main__':
    print("### Testing Scorer Logic ###")
    print("-" * 30)
    
    # Example data (these would typically be outputs from other modules)
    sample_resume_keywords = ["python", "django", "api", "web development", "javascript"]
    sample_jd_keywords_good_match = ["python", "django", "backend", "api", "rest", "web services"]
    sample_jd_keywords_poor_match = ["java", "spring", "microservices", "sql"]
    
    semantic_score_good = 0.85  # Example high semantic similarity
    semantic_score_fair = 0.60  # Example fair semantic similarity
    semantic_score_poor = 0.30  # Example low semantic similarity
    
    # --- Test Case 1: Good keyword match, good semantic similarity ---
    print("\n--- Test Case 1: Good Match ---")
    overall_score_1 = calculate_overall_score(
        sample_resume_keywords,
        sample_jd_keywords_good_match,
        semantic_score_good
    )
    keyword_match_1 = calculate_keyword_match_score(sample_resume_keywords, sample_jd_keywords_good_match)
    
    print(f"Resume Keywords: {sample_resume_keywords}")
    print(f"JD Keywords: {sample_jd_keywords_good_match}")
    print(f"Keyword Match Score (Jaccard): {keyword_match_1:.4f}")
    print(f"Semantic Similarity Score: {semantic_score_good:.4f}")
    print(f"Overall Score: {overall_score_1:.2f}/100")
    print("-" * 30)
    
    # --- Test Case 2: Poor keyword match, fair semantic similarity ---
    print("\n--- Test Case 2: Poor Keyword Match, Fair Semantic ---")
    overall_score_2 = calculate_overall_score(
        sample_resume_keywords,
        sample_jd_keywords_poor_match,
        semantic_score_fair
    )
    keyword_match_2 = calculate_keyword_match_score(sample_resume_keywords, sample_jd_keywords_poor_match)
    
    print(f"Resume Keywords: {sample_resume_keywords}")
    print(f"JD Keywords: {sample_jd_keywords_poor_match}")
    print(f"Keyword Match Score (Jaccard): {keyword_match_2:.4f}")
    print(f"Semantic Similarity Score: {semantic_score_fair:.4f}")
    print(f"Overall Score: {overall_score_2:.2f}/100")
    print("-" * 30)
    
    # --- Test Case 3: Good keyword match, poor semantic similarity ---
    # (This scenario might be less common if keywords are well-chosen and semantics align)
    print("\n--- Test Case 3: Good Keywords, Poor Semantic ---")
    overall_score_3 = calculate_overall_score(
        sample_resume_keywords,
        sample_jd_keywords_good_match,  # Using good match keywords
        semantic_score_poor  # But poor semantic score
    )
    keyword_match_3 = calculate_keyword_match_score(sample_resume_keywords, sample_jd_keywords_good_match)
    
    print(f"Resume Keywords: {sample_resume_keywords}")
    print(f"JD Keywords: {sample_jd_keywords_good_match}")
    print(f"Keyword Match Score (Jaccard): {keyword_match_3:.4f}")
    print(f"Semantic Similarity Score: {semantic_score_poor:.4f}")
    print(f"Overall Score: {overall_score_3:.2f}/100")
    print("-" * 30)
    
    # --- Test Case 4: Custom weights ---
    print("\n--- Test Case 4: Custom Weights (more emphasis on keywords) ---")
    overall_score_4 = calculate_overall_score(
        sample_resume_keywords,
        sample_jd_keywords_good_match,
        semantic_score_good,
        keyword_weight=0.7,  # More weight to keywords
        semantic_weight=0.3
    )
    print(f"Overall Score (70% Keyword, 30% Semantic): {overall_score_4:.2f}/100")
    print("-" * 30)
    
    # --- Test Case 5: Edge case - empty keywords ---
    print("\n--- Test Case 5: Empty Keywords ---")
    overall_score_5 = calculate_overall_score(
        [],  # Empty resume keywords
        sample_jd_keywords_good_match,
        semantic_score_good
    )
    keyword_match_5 = calculate_keyword_match_score([], sample_jd_keywords_good_match)
    
    print(f"Resume Keywords: []")
    print(f"JD Keywords: {sample_jd_keywords_good_match}")
    print(f"Keyword Match Score (Jaccard): {keyword_match_5:.4f}")
    print(f"Semantic Similarity Score: {semantic_score_good:.4f}")
    print(f"Overall Score: {overall_score_5:.2f}/100")
    
    overall_score_6 = calculate_overall_score(
        sample_resume_keywords,
        [],  # Empty JD keywords
        semantic_score_good
    )
    print(f"Overall Score (Empty JD Keywords): {overall_score_6:.2f}/100")
    print("-" * 30)
    
    # --- Test Case 6: Weights not summing to 1 (should normalize) ---
    print("\n--- Test Case 6: Weights not summing to 1 ---")
    overall_score_7 = calculate_overall_score(
        sample_resume_keywords,
        sample_jd_keywords_good_match,
        semantic_score_good,
        keyword_weight=0.5,
        semantic_weight=0.8  # Sum = 1.3
    )
    # Expected effective weights after normalization: kw = 0.5/1.3, sw = 0.8/1.3
    # kw_eff = 0.3846, sw_eff = 0.6153
    # score = (kw_match * 0.3846 + sem_score * 0.6153) * 100
    # kw_match_1 = 0.375
    # score = (0.375 * 0.3846 + 0.85 * 0.6153) * 100 = (0.144225 + 0.523005) * 100 = 0.66723 * 100 = 66.72
    print(f"Overall Score (weights 0.5, 0.8): {overall_score_7:.2f}/100")
    print("-" * 30)
