# How to run this Streamlit application:
# 1. Ensure the backend FastAPI server is running.
#    Navigate to the project's root directory and run:
#    uvicorn backend.main:app --reload
#    (The backend should be accessible at http://127.0.0.1:8000)
#
# 2. Open a new terminal, navigate to the project's root directory.
# 3. Run this Streamlit app using the command:
#    streamlit run frontend/app.py
#
# 4. The Streamlit app will open in your web browser (usually at http://localhost:8501).

import streamlit as st
import requests
import json  # For more robust JSON parsing if needed, though requests.json() is usually enough
import os  # To read environment variables
import tempfile

# Configuration for Backend API URLs
# Reads from environment variable 'BACKEND_API_URL' if set (e.g., by Docker Compose),
# otherwise defaults to localhost for local development.
BACKEND_API_BASE_URL = os.environ.get("BACKEND_API_URL", "http://127.0.0.1:8000")
BACKEND_TEXT_API_URL = f"{BACKEND_API_BASE_URL}/analyze_resume/"
BACKEND_FILES_API_URL = f"{BACKEND_API_BASE_URL}/analyze_resume_files/"

# --- UI Design ---
st.set_page_config(page_title="Smart Resume Analyzer", layout="wide")
st.title("📄 Smart Resume Analyzer")

st.markdown("""
Welcome to the Smart Resume Analyzer! Paste your resume and a job description below or upload files to get a comprehensive analysis of how well they match.
""")

st.sidebar.header("Instructions")
st.sidebar.info("""
**Text Input Method:**
1. Paste the full text of your resume into the 'Resume Text' box.
2. Paste the full text of the job description into the 'Job Description Text' box.
3. Click the 'Analyze Resume' button.

**File Upload Method:**
1. Upload your resume file (PDF, DOCX, or TXT).
2. Upload the job description file (PDF, DOCX, or TXT).
3. Click the 'Analyze Files' button.

The analysis results, including a match score and feedback, will be displayed below.
""")

st.sidebar.warning("Ensure the backend server is running for the analysis to work.")

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

st.divider()

# Add file upload section
st.subheader("📄 Or Upload Files")
file_col1, file_col2 = st.columns(2)

with file_col1:
    resume_file = st.file_uploader(
        "Upload Resume (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"]
    )

with file_col2:
    job_description_file = st.file_uploader(
        "Upload Job Description (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"]
    )

st.divider()

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "error_message" not in st.session_state:
    st.session_state.error_message = None

# Text analysis button
text_col1, text_col2 = st.columns(2)
with text_col1:
    if st.button("🚀 Analyze Text Input", type="primary", use_container_width=True):
        st.session_state.analysis_result = None  # Reset previous results
        st.session_state.error_message = None

        if not resume_text or not job_description_text:
            st.session_state.error_message = (
                "⚠️ Please paste both the resume and job description text."
            )
        else:
            payload = {
                "resume_text": resume_text,
                "job_description_text": job_description_text,
            }

            try:
                with st.spinner("Analyzing text input... This may take a moment. 🧠"):
                    response = requests.post(
                        BACKEND_TEXT_API_URL, json=payload, timeout=120
                    )  # Increased timeout

                    if response.status_code == 200:
                        st.session_state.analysis_result = response.json()
                    else:
                        try:
                            error_detail = response.json().get("detail", response.text)
                        except json.JSONDecodeError:
                            error_detail = response.text

                        st.session_state.error_message = f"⚠️ Error from backend (HTTP {response.status_code}): {error_detail}"

            except requests.exceptions.ConnectionError:
                st.session_state.error_message = f"⚠️ Connection Error: Could not connect to the backend API at {BACKEND_TEXT_API_URL}. Please ensure the backend server is running."
            except requests.exceptions.Timeout:
                st.session_state.error_message = (
                    "⚠️ Request timed out. The backend took too long to respond."
                )
            except Exception as e:
                st.session_state.error_message = (
                    f"⚠️ An unexpected error occurred: {str(e)}"
                )

# File analysis button
with text_col2:
    if st.button("📄 Analyze Uploaded Files", type="primary", use_container_width=True):
        st.session_state.analysis_result = None  # Reset previous results
        st.session_state.error_message = None

        if not resume_file or not job_description_file:
            st.session_state.error_message = (
                "⚠️ Please upload both resume and job description files."
            )
        else:
            try:
                with st.spinner(
                    "Analyzing uploaded files... This may take a moment. 🧠"
                ):
                    files = {
                        "resume_file": (
                            resume_file.name,
                            resume_file.getvalue(),
                            resume_file.type,
                        ),
                        "job_description_file": (
                            job_description_file.name,
                            job_description_file.getvalue(),
                            job_description_file.type,
                        ),
                    }

                    response = requests.post(
                        BACKEND_FILES_API_URL, files=files, timeout=120
                    )

                    if response.status_code == 200:
                        st.session_state.analysis_result = response.json()
                    else:
                        try:
                            error_detail = response.json().get("detail", response.text)
                        except json.JSONDecodeError:
                            error_detail = response.text

                        st.session_state.error_message = f"⚠️ Error from backend (HTTP {response.status_code}): {error_detail}"

            except requests.exceptions.ConnectionError:
                st.session_state.error_message = f"⚠️ Connection Error: Could not connect to the backend API at {BACKEND_FILES_API_URL}. Please ensure the backend server is running."
            except requests.exceptions.Timeout:
                st.session_state.error_message = (
                    "⚠️ Request timed out. The backend took too long to respond."
                )
            except Exception as e:
                st.session_state.error_message = (
                    f"⚠️ An unexpected error occurred: {str(e)}"
                )

# --- Display Results or Errors ---
if st.session_state.error_message:
    # Ensure the error message (which might include Request ID from backend) is clearly shown
    st.error(f"An error occurred: {st.session_state.error_message}")

if st.session_state.analysis_result:
    st.subheader("🔍 Analysis Results")
    results = st.session_state.analysis_result

    # --- Display Scores ---
    overall_score = results.get("overall_score", 0.0)
    semantic_score = results.get("semantic_similarity_score", 0.0)
    keyword_score = results.get("keyword_match_score", 0.0)

    st.metric(label="Overall Match Score", value=f"{overall_score:.2f}/100")

    score_col1, score_col2 = st.columns(2)
    with score_col1:
        st.markdown("**Semantic Similarity**")
        st.progress(int(semantic_score * 100), text=f"{semantic_score * 100:.1f}%")

    with score_col2:
        st.markdown("**Keyword Match**")
        st.progress(int(keyword_score * 100), text=f"{keyword_score * 100:.1f}%")

    st.divider()

    # --- Display Structured Feedback ---
    st.subheader("💡 Detailed Feedback")
    feedback_data = results.get("feedback", {})

    summary = feedback_data.get("overall_summary", [])
    if summary:
        # st.subheader("Summary")  # Already have "Detailed Feedback"
        for item in summary:
            st.markdown(f"**{item}**")  # Make summary bold
        st.markdown("")  # Add a little space

    strengths = feedback_data.get("strengths", [])
    if strengths:
        with st.expander("✅ Strengths", expanded=True):
            for item in strengths:
                st.markdown(f"- {item}")

    improvements = feedback_data.get("areas_for_improvement", [])
    if improvements:
        with st.expander("🛠️ Areas for Improvement", expanded=True):
            for item in improvements:
                st.markdown(f"- {item}")

    missing_keywords_sugg = feedback_data.get("missing_keywords_suggestions", [])
    if missing_keywords_sugg:
        with st.expander("🔑 Missing Keyword Suggestions", expanded=False):
            for item in missing_keywords_sugg:
                st.markdown(f"- {item}")

    # Example of how to access other potential feedback parts if they were added
    # other_feedback = feedback_data.get("other_notes", [])
    # if other_feedback:
    #     with st.expander("📝 Other Notes"):
    #         for item in other_feedback:
    #             st.markdown(f"- {item}")

    # Remove raw JSON display for cleaner UI, or keep it under an expander for debugging
    # with st.expander("Raw Backend Response (for debugging)"):
    #     st.json(results)

st.markdown("---")
st.markdown("from Hasif's Workspace")
