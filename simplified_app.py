import streamlit as st
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Simple text preprocessing functions
def preprocess_text(text):
    """Simple text preprocessing without NLTK"""
    if not isinstance(text, str):
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator)

    # Remove extra whitespace
    text = " ".join(text.split())

    return text


def extract_keywords(text, top_n=10):
    """Extract keywords using TF-IDF"""
    if not text:
        return []

    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words="english")

    # Fit and transform the text
    tfidf_matrix = vectorizer.fit_transform([text])

    # Get feature names
    feature_names = vectorizer.get_feature_names_out()

    # Get sorted indices of TF-IDF scores
    sorted_indices = tfidf_matrix.toarray()[0].argsort()[::-1]

    # Get top keywords
    keywords = []
    for idx in sorted_indices[:top_n]:
        if tfidf_matrix[0, idx] > 0:
            keywords.append(feature_names[idx])

    return keywords


def calculate_similarity(text1, text2):
    """Calculate cosine similarity between two texts"""
    if not text1 or not text2:
        return 0.0

    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer(stop_words="english")

    # Fit and transform both texts
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    # Calculate cosine similarity
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    return similarity


def calculate_keyword_match(resume_keywords, jd_keywords):
    """Calculate keyword match score"""
    if not resume_keywords or not jd_keywords:
        return 0.0

    # Convert to sets
    resume_set = set(resume_keywords)
    jd_set = set(jd_keywords)

    # Calculate Jaccard similarity
    intersection = len(resume_set.intersection(jd_set))
    union = len(resume_set.union(jd_set))

    if union == 0:
        return 0.0

    return intersection / union


def calculate_overall_score(
    keyword_match, similarity, keyword_weight=0.4, similarity_weight=0.6
):
    """Calculate overall score"""
    # Ensure weights sum to 1
    total_weight = keyword_weight + similarity_weight
    if total_weight != 1.0:
        keyword_weight /= total_weight
        similarity_weight /= total_weight

    # Calculate weighted score
    score = (keyword_match * keyword_weight) + (similarity * similarity_weight)

    # Scale to 0-100
    return score * 100


def generate_feedback(resume_keywords, jd_keywords, similarity, overall_score):
    """Generate feedback based on analysis"""
    feedback = {
        "overall_summary": [],
        "strengths": [],
        "areas_for_improvement": [],
        "missing_keywords_suggestions": [],
    }

    # Identify missing keywords
    resume_set = set(resume_keywords)
    jd_set = set(jd_keywords)
    missing_keywords = list(jd_set - resume_set)

    if missing_keywords:
        top_missing = missing_keywords[:5]
        feedback["missing_keywords_suggestions"].append(
            f"Consider incorporating these keywords from the job description: {', '.join(top_missing)}."
        )

    # Generate overall summary
    if overall_score >= 75:
        feedback["overall_summary"].append(
            f"Excellent match! Your resume aligns well with the job description (Score: {overall_score:.0f}/100)."
        )
    elif overall_score >= 50:
        feedback["overall_summary"].append(
            f"Good potential! Your resume shows reasonable alignment with the job description (Score: {overall_score:.0f}/100)."
        )
    else:
        feedback["overall_summary"].append(
            f"Needs improvement. Your resume could be better aligned with this job description (Score: {overall_score:.0f}/100)."
        )

    # Generate strengths
    common_keywords = list(resume_set.intersection(jd_set))
    if common_keywords:
        feedback["strengths"].append(
            f"Your resume effectively highlights skills like: {', '.join(common_keywords[:5])}, which are also mentioned in the job description."
        )

    if similarity >= 0.7:
        feedback["strengths"].append(
            "Your resume shows strong semantic alignment with the job description."
        )

    # Generate areas for improvement
    if similarity < 0.5:
        feedback["areas_for_improvement"].append(
            "Consider rephrasing your experience to better match the language used in the job description."
        )

    if len(missing_keywords) > 5:
        feedback["areas_for_improvement"].append(
            "There are several keywords from the job description missing in your resume."
        )

    return feedback


# Streamlit UI
st.set_page_config(page_title="Simple Resume Analyzer", layout="wide")
st.title("📄 Simple Resume Analyzer")

st.markdown("""
Welcome to the Simple Resume Analyzer! Paste your resume and a job description below to get an analysis of how well they match.
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Your Resume")
    resume_text = st.text_area(
        "Paste your full resume text here:",
        height=400,
        key="resume_text_area",
        placeholder="E.g., John Doe\nExperienced Python Developer...",
    )

with col2:
    st.subheader("🎯 Job Description")
    job_description_text = st.text_area(
        "Paste the full job description text here:",
        height=400,
        key="jd_text_area",
        placeholder="E.g., We are looking for a Senior Software Engineer...",
    )

if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
    if not resume_text or not job_description_text:
        st.error("⚠️ Please paste both the resume and job description text.")
    else:
        with st.spinner("Analyzing... This may take a moment. 🧠"):
            # Preprocess texts
            processed_resume = preprocess_text(resume_text)
            processed_jd = preprocess_text(job_description_text)

            # Extract keywords
            resume_keywords = extract_keywords(processed_resume, top_n=15)
            jd_keywords = extract_keywords(processed_jd, top_n=15)

            # Calculate similarity
            similarity = calculate_similarity(processed_resume, processed_jd)

            # Calculate keyword match
            keyword_match = calculate_keyword_match(resume_keywords, jd_keywords)

            # Calculate overall score
            overall_score = calculate_overall_score(keyword_match, similarity)

            # Generate feedback
            feedback = generate_feedback(
                resume_keywords, jd_keywords, similarity, overall_score
            )

            # Display results
            st.subheader("🔍 Analysis Results")

            # Display scores
            st.metric(label="Overall Match Score", value=f"{overall_score:.2f}/100")

            score_col1, score_col2 = st.columns(2)
            with score_col1:
                st.markdown("**Semantic Similarity**")
                st.progress(int(similarity * 100), text=f"{similarity * 100:.1f}%")

            with score_col2:
                st.markdown("**Keyword Match**")
                st.progress(
                    int(keyword_match * 100), text=f"{keyword_match * 100:.1f}%"
                )

            st.divider()

            # Display feedback
            st.subheader("💡 Detailed Feedback")

            # Display summary
            summary = feedback.get("overall_summary", [])
            if summary:
                for item in summary:
                    st.markdown(f"**{item}**")
                st.markdown("")

            # Display strengths
            strengths = feedback.get("strengths", [])
            if strengths:
                with st.expander("✅ Strengths", expanded=True):
                    for item in strengths:
                        st.markdown(f"- {item}")

            # Display areas for improvement
            improvements = feedback.get("areas_for_improvement", [])
            if improvements:
                with st.expander("🛠️ Areas for Improvement", expanded=True):
                    for item in improvements:
                        st.markdown(f"- {item}")

            # Display missing keywords
            missing_keywords = feedback.get("missing_keywords_suggestions", [])
            if missing_keywords:
                with st.expander("🔑 Missing Keyword Suggestions", expanded=False):
                    for item in missing_keywords:
                        st.markdown(f"- {item}")

            # Display extracted keywords
            with st.expander("🔤 Extracted Keywords", expanded=False):
                st.markdown("**Resume Keywords:**")
                st.write(", ".join(resume_keywords))
                st.markdown("**Job Description Keywords:**")
                st.write(", ".join(jd_keywords))

st.markdown("---")
st.markdown("from Hasif's Workspace")
