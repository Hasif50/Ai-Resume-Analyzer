# Ai Resume Analyzer

A powerful tool to screen resumes and match candidates to job descriptions efficiently.

This project leverages Natural Language Processing (NLP) techniques to analyze resumes against job descriptions, providing a compatibility score and actionable feedback. It aims to streamline the initial screening process for recruiters and help candidates tailor their resumes for better job matches.

## ✨ Features

- **Automated Resume Parsing:** Extracts text from PDF and DOCX resume files (core parsing scripts developed).
- **Job Description Parsing:** Extracts text from PDF, DOCX, and TXT job description files (core parsing scripts developed).
- **Text Preprocessing:** Cleans and prepares text data using techniques like lowercasing, punctuation removal, stopword removal, and lemmatization.
- **Keyword Extraction:** Identifies key terms from resumes and job descriptions using TF-IDF and spaCy's noun chunking.
- **Semantic Similarity Analysis:** Calculates the contextual similarity between resume and job description using Sentence Transformers.
- **Scoring Mechanism:** Provides an overall compatibility score based on weighted keyword match and semantic similarity.
- **Actionable Feedback:** Generates feedback highlighting strengths, areas for improvement, and missing keywords.
- **FastAPI Backend:** Exposes NLP functionalities through a robust REST API.
- **Streamlit Frontend:** Offers a user-friendly web interface for easy interaction.
- **Dockerized Deployment:** Includes Dockerfiles for containerizing backend and frontend services, with a `docker-compose.yml` for easy local orchestration.

## 🛠️ Tech Stack

- **Backend:**
  - Python 3.10+
  - FastAPI: For building the REST API.
  - Uvicorn: ASGI server for FastAPI.
  - spaCy: For advanced NLP tasks (lemmatization, noun chunks).
  - NLTK: For text preprocessing (tokenization, stopwords).
  - Scikit-learn: For TF-IDF keyword extraction and cosine similarity.
  - Sentence Transformers: For generating text embeddings and semantic similarity.
  - PyTorch (CPU): As a dependency for Sentence Transformers.
  - PyPDF2 & python-docx: For parsing PDF and DOCX files.
- **Frontend:**
  - Streamlit: For creating the interactive web application.
  - Requests: For communicating with the backend API.
- **Containerization:**
  - Docker & Docker Compose

## 📂 Project Structure

```
├── backend/                # FastAPI application, NLP modules, Dockerfile
│   ├── __init__.py
│   ├── main.py             # FastAPI app definition and endpoints
│   ├── text_processor.py   # Text preprocessing functions
│   ├── keyword_extractor.py # Keyword extraction functions
│   ├── semantic_analyzer.py # Semantic similarity calculation
│   ├── scorer.py           # Scoring logic
│   ├── feedback_generator.py # Feedback generation logic
│   ├── requirements.txt    # Backend Python dependencies
│   └── Dockerfile          # Dockerfile for backend
├── frontend/               # Streamlit application, Dockerfile
│   ├── app.py              # Streamlit application code
│   ├── requirements.txt    # Frontend Python dependencies
│   └── Dockerfile          # Dockerfile for frontend
├── docker-compose.yml      # Docker Compose file for easy local orchestration
└── README.md               # This file
```

## ⚙️ Setup and Installation

### Prerequisites

- Python 3.10 or later.
- `pip` (Python package installer).
- Docker and Docker Compose (recommended for easiest setup, optional for local dev).

### Option 1: Using Docker (Recommended)

1. Clone this repository:
   ```
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Build and start the services with Docker Compose:
   ```
   docker-compose up --build
   ```

3. Access the application:
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Option 2: Local Development

1. Clone this repository:
   ```
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Set up the backend:
   ```
   cd backend
   python -m venv venv
   # On Windows:
   # venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   pip install -r requirements.txt
   python -m nltk.downloader punkt stopwords wordnet averaged_perceptron_tagger
   python -m spacy download en_core_web_sm
   cd ..
   ```

3. Set up the frontend:
   ```
   cd frontend
   python -m venv venv
   # On Windows:
   # venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   pip install -r requirements.txt
   cd ..
   ```

4. Start the backend server:
   ```
   # From the project root
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. In a new terminal, start the frontend:
   ```
   # From the project root
   streamlit run frontend/app.py
   ```

6. Access the application:
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📖 User Guide

### Text Input Method
1. Access the application at http://localhost:8501
2. Paste your resume text in the left text area
3. Paste the job description text in the right text area
4. Click "Analyze Text Input"
5. Review the analysis results

### File Upload Method
1. Access the application at http://localhost:8501
2. Upload your resume file (PDF, DOCX, or TXT) in the resume upload section
3. Upload the job description file (PDF, DOCX, or TXT) in the job description upload section
4. Click "Analyze Uploaded Files"
5. Review the analysis results

### Analysis Results Include
- Overall Match Score
- Semantic Similarity and Keyword Match scores
- Detailed feedback with strengths, areas for improvement, and missing keyword suggestions
- Extracted keywords from both resume and job description

## 🔌 API Usage

The backend provides a REST API for resume analysis with two main endpoints.

### Endpoint 1: `/analyze_resume/` (Text Input)

- **Method:** `POST`
- **URL:** `http://localhost:8000/analyze_resume/`
- **Request Body (JSON):**
  ```json
  {
    "resume_text": "Full text of the resume...",
    "job_description_text": "Full text of the job description..."
  }
  ```
- **Response (JSON):**
  ```json
  {
    "overall_score": 75.5,
    "semantic_similarity_score": 0.82,
    "keyword_match_score": 0.65,
    "resume_keywords": ["python", "api", "django"],
    "jd_keywords": ["python", "api", "fastapi"],
    "feedback": {
      "overall_summary": ["Detailed summary of the match..."],
      "strengths": ["List of identified strengths..."],
      "areas_for_improvement": ["Suggestions for improvement..."],
      "missing_keywords_suggestions": ["Keywords from JD missing in resume..."]
    }
  }
  ```

### Endpoint 2: `/analyze_resume_files/` (File Upload)

- **Method:** `POST`
- **URL:** `http://localhost:8000/analyze_resume_files/`
- **Request Body (Multipart Form):**
  - `resume_file`: PDF, DOCX, or TXT file
  - `job_description_file`: PDF, DOCX, or TXT file
- **Response (JSON):** Same format as the `/analyze_resume/` endpoint

## License

This project is licensed under the MIT License - see the LICENSE file for details.
