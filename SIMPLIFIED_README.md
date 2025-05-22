# Smart Resume Analyzer with AI (Simplified Version)

An AI-powered tool to screen resumes and match candidates to job descriptions efficiently.

This project uses Natural Language Processing (NLP) techniques to analyze resumes against job descriptions, providing a compatibility score and actionable feedback. It aims to streamline the initial screening process for recruiters and help candidates tailor their resumes.

## ✨ Features

- **Text Preprocessing:** Cleans and prepares text data using techniques like lowercasing and punctuation removal.
- **Keyword Extraction:** Identifies key terms from resumes and job descriptions using TF-IDF.
- **Semantic Similarity Analysis:** Calculates the contextual similarity between resume and job description.
- **Scoring Mechanism:** Provides an overall compatibility score based on weighted keyword match and semantic similarity.
- **Actionable Feedback:** Generates feedback highlighting strengths, areas for improvement, and missing keywords.
- **Streamlit Frontend:** Offers a user-friendly web interface for easy interaction.
- **Dockerized Deployment:** Includes Dockerfile and docker-compose.yml for easy containerization.

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit:** For creating the interactive web application.
- **Scikit-learn:** For TF-IDF keyword extraction and cosine similarity.
- **Docker & Docker Compose**

## 📂 Project Structure

```
├── simplified_app.py      # Streamlit application with all functionality
├── sample_resume.txt      # Sample resume for testing
├── sample_job_description.txt # Sample job description for testing
├── requirements.txt       # Python dependencies
├── Dockerfile             # Dockerfile for containerization
└── simple-docker-compose.yml # Docker Compose file for easy orchestration
```

## ⚙️ Setup and Installation

### Option 1: Using Docker (Recommended)

1. Build and start the service with Docker Compose:
   ```
   docker-compose -f simple-docker-compose.yml up --build
   ```

2. Access the application at http://localhost:8501

### Option 2: Local Development

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the Streamlit app:
   ```
   streamlit run simplified_app.py
   ```

3. Access the application at http://localhost:8501

## 📖 User Guide

1. Access the application at http://localhost:8501
2. Paste your resume text in the left text area
3. Paste the job description text in the right text area
4. Click "Analyze Resume"
5. Review the analysis results:
   - Overall Match Score
   - Semantic Similarity and Keyword Match scores
   - Detailed feedback with strengths, areas for improvement, and missing keyword suggestions

## License

This project is licensed under the MIT License.
