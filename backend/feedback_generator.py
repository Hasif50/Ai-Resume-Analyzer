import sys
import os

# Add the parent directory (project root) to sys.path to resolve imports like 'from backend.module'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# For example usage, we might want to use the scorer or other components
# from backend.scorer import calculate_overall_score, calculate_keyword_match_score

def generate_feedback(resume_keywords, jd_keywords, semantic_similarity_score, overall_score, top_n_missing_keywords=5):
    """
    Generates actionable feedback based on resume analysis against a job description.
    
    Args:
        resume_keywords (list of str): Keywords extracted from the resume.
        jd_keywords (list of str): Keywords extracted from the job description.
        semantic_similarity_score (float): The semantic similarity score (0 to 1).
        overall_score (float): The overall compatibility score (0 to 100).
        top_n_missing_keywords (int): The number of top missing keywords to suggest.
    
    Returns:
        dict: A dictionary containing different pieces of feedback, e.g.,
              {'overall_summary': str, 'missing_keywords': list, 'strengths': list, 'suggestions': list}
    """
    feedback = {
        'overall_summary': [],  # Initialize as a list
        'missing_keywords_suggestions': [],
        'strengths': [],
        'areas_for_improvement': []
    }
    
    # 1. Identify missing keywords
    set_resume_keywords = set(k.lower() for k in resume_keywords)
    set_jd_keywords = set(k.lower() for k in jd_keywords)
    missing_keywords = list(set_jd_keywords - set_resume_keywords)
    
    if missing_keywords:
        suggestion = f"Consider incorporating relevant keywords from the job description that are currently less prominent in your resume. For example: {', '.join(missing_keywords[:top_n_missing_keywords])}."
        feedback['missing_keywords_suggestions'].append(suggestion)
        
        if len(missing_keywords) > top_n_missing_keywords:
            feedback['missing_keywords_suggestions'].append(f"There are {len(missing_keywords) - top_n_missing_keywords} more keywords from the job description worth reviewing.")
    
    # 2. Generate overall summary based on scores
    if overall_score >= 75:
        feedback['overall_summary'].append(f"Excellent match! Your resume aligns very well with the job description (Overall Score: {overall_score:.0f}/100).")
        
        if semantic_similarity_score >= 0.75:
            feedback['strengths'].append("Your resume shows strong semantic alignment with the core responsibilities and skills outlined in the job description.")
        elif semantic_similarity_score >= 0.60:
            feedback['strengths'].append("Good semantic alignment with the job description.")
    
    elif overall_score >= 50:
        feedback['overall_summary'].append(f"Good potential! Your resume shows a reasonable alignment with the job description (Overall Score: {overall_score:.0f}/100).")
        
        if semantic_similarity_score >= 0.60:
            feedback['strengths'].append("Your resume's content is generally well-aligned with the job description's key aspects.")
        else:
            feedback['areas_for_improvement'].append("While there's some overlap, consider tailoring your language to better reflect the specific terminology and focus areas of the job description to improve semantic relevance.")
    
    else:  # overall_score < 50
        feedback['overall_summary'].append(f"Needs improvement. Your resume could be better aligned with this specific job description (Overall Score: {overall_score:.0f}/100).")
        
        if semantic_similarity_score < 0.5:
            feedback['areas_for_improvement'].append("Focus on rephrasing your experience and skills to more closely match the language and requirements of the job description. The semantic similarity is currently low.")
        else:
            feedback['areas_for_improvement'].append("Review the job description carefully and ensure your resume clearly highlights the most relevant skills and experiences.")
    
    # 3. Specific suggestions based on keywords and semantic score
    common_keywords = list(set_resume_keywords.intersection(set_jd_keywords))
    if common_keywords:
        feedback['strengths'].append(f"Your resume effectively highlights skills like: {', '.join(common_keywords[:top_n_missing_keywords])}, which are also mentioned in the job description.")
    
    if not missing_keywords and overall_score >= 70:
        feedback['strengths'].append("Great keyword coverage! Your resume appears to include many of the key terms from the job description.")
    
    if not feedback['strengths'] and overall_score >=60 :
        feedback['strengths'].append("Your resume shows a good overall match. Ensure specific examples of your achievements are clearly presented.")
    
    if not feedback['missing_keywords_suggestions'] and overall_score < 70 :
        feedback['areas_for_improvement'].append("Review the job description for any specific skills or qualifications you possess but haven't explicitly mentioned or emphasized in your resume.")
    
    # Consolidate feedback if some lists are empty
    if not feedback['strengths']:
        feedback.pop('strengths')
    
    if not feedback['areas_for_improvement']:
        feedback.pop('areas_for_improvement')
    
    if not feedback['missing_keywords_suggestions']:
        feedback.pop('missing_keywords_suggestions')
    
    return feedback

if __name__ == '__main__':
    print("### Testing Feedback Generation ###")
    print("-" * 40)
    
    # --- Scenario 1: High score, good match ---
    print("\n--- Scenario 1: High Score, Good Match ---")
    resume_kw_1 = ["python", "django", "api", "web development", "machine learning", "data analysis"]
    jd_kw_1 = ["python", "django", "api", "restful services", "machine learning", "problem solving"]
    sem_score_1 = 0.85
    overall_score_1 = 88.0
    
    feedback_1 = generate_feedback(resume_kw_1, jd_kw_1, sem_score_1, overall_score_1)
    
    print(f"Resume Keywords: {resume_kw_1}")
    print(f"JD Keywords: {jd_kw_1}")
    print(f"Semantic Score: {sem_score_1}, Overall Score: {overall_score_1}")
    
    for key, value in feedback_1.items():
        if isinstance(value, list) and value:
            print(f"{key.replace('_', ' ').title()}:")
            for item in value:
                print(f" - {item}")
        elif isinstance(value, str) and value:
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("-" * 40)
    
    # --- Scenario 2: Medium score, some missing keywords ---
    print("\n--- Scenario 2: Medium Score, Missing Keywords ---")
    resume_kw_2 = ["java", "spring boot", "sql", "backend development"]
    jd_kw_2 = ["java", "spring", "microservices", "api design", "cloud (aws/azure)", "kubernetes"]
    sem_score_2 = 0.60
    overall_score_2 = 55.0
    
    feedback_2 = generate_feedback(resume_kw_2, jd_kw_2, sem_score_2, overall_score_2, top_n_missing_keywords=3)
    
    print(f"Resume Keywords: {resume_kw_2}")
    print(f"JD Keywords: {jd_kw_2}")
    print(f"Semantic Score: {sem_score_2}, Overall Score: {overall_score_2}")
    
    for key, value in feedback_2.items():
        if isinstance(value, list) and value:
            print(f"{key.replace('_', ' ').title()}:")
            for item in value:
                print(f" - {item}")
        elif isinstance(value, str) and value:
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("-" * 40)
    
    # --- Scenario 3: Low score, significant mismatch ---
    print("\n--- Scenario 3: Low Score, Mismatch ---")
    resume_kw_3 = ["marketing", "social media", "content creation"]
    jd_kw_3 = ["software engineer", "c++", "systems programming", "algorithms"]
    sem_score_3 = 0.20
    overall_score_3 = 15.0
    
    feedback_3 = generate_feedback(resume_kw_3, jd_kw_3, sem_score_3, overall_score_3)
    
    print(f"Resume Keywords: {resume_kw_3}")
    print(f"JD Keywords: {jd_kw_3}")
    print(f"Semantic Score: {sem_score_3}, Overall Score: {overall_score_3}")
    
    for key, value in feedback_3.items():
        if isinstance(value, list) and value:
            print(f"{key.replace('_', ' ').title()}:")
            for item in value:
                print(f" - {item}")
        elif isinstance(value, str) and value:
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("-" * 40)
    
    # --- Scenario 4: Good score but some important keywords missing ---
    print("\n--- Scenario 4: Good Score, Few Important Missing Keywords ---")
    resume_kw_4 = ["python", "api", "web development", "javascript"]  # Missing "django" and "machine learning"
    jd_kw_4 = ["python", "django", "api", "machine learning", "web development"]
    sem_score_4 = 0.78
    overall_score_4 = 70.0  # Score penalized slightly by missing keywords via keyword_score component
    
    feedback_4 = generate_feedback(resume_kw_4, jd_kw_4, sem_score_4, overall_score_4, top_n_missing_keywords=2)
    
    print(f"Resume Keywords: {resume_kw_4}")
    print(f"JD Keywords: {jd_kw_4}")
    print(f"Semantic Score: {sem_score_4}, Overall Score: {overall_score_4}")
    
    for key, value in feedback_4.items():
        if isinstance(value, list) and value:
            print(f"{key.replace('_', ' ').title()}:")
            for item in value:
                print(f" - {item}")
        elif isinstance(value, str) and value:
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("-" * 40)
