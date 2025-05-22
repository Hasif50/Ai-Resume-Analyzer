import sys
import os
from typing import List, Dict, Any

# Add the parent directory (project root) to sys.path to resolve imports from 'backend'
# This is important for when Uvicorn runs this file and for importing local backend modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import (
    FastAPI,
    HTTPException,
    Request as FastAPIRequest,
    UploadFile,
    File,
    Form,
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import logging
import uuid  # For generating unique request IDs
import tempfile
import shutil

from backend.semantic_analyzer import (
    sentence_model as global_sentence_model,
)  # To check if model loaded

# --- Logging Setup ---
# Ensure the log file is created within the 'backend' directory, regardless of where uvicorn is run from.
LOG_FILE_NAME = "backend_app.log"
BACKEND_DIR = os.path.dirname(__file__)
ABSOLUTE_LOG_FILE_PATH = os.path.join(BACKEND_DIR, LOG_FILE_NAME)

logger = logging.getLogger("api_logger")  # Specific name for our logger
logger.setLevel(logging.INFO)  # Default level

# Create handlers
# Use absolute path for FileHandler
file_handler = logging.FileHandler(ABSOLUTE_LOG_FILE_PATH)
file_handler.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Can be set to DEBUG for more console verbosity

# Create formatter and add it to handlers
# Adding %(module)s and %(lineno)d for more detailed logging
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(request_id)s - [%(module)s:%(lineno)d] - %(message)s"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
# Check if handlers already exist to prevent duplication if uvicorn reloads or script is run multiple times
if not logger.handlers:  # Simpler check: if no handlers, add them.
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
else:
    # If handlers exist, ensure they are the correct ones (more robust for complex scenarios)
    has_file_handler = any(
        isinstance(h, logging.FileHandler) and h.baseFilename == ABSOLUTE_LOG_FILE_PATH
        for h in logger.handlers
    )
    has_console_handler = any(
        isinstance(h, logging.StreamHandler) for h in logger.handlers
    )

    if not has_file_handler:
        logger.addHandler(file_handler)
    if not has_console_handler:
        logger.addHandler(console_handler)


# --- Pydantic Models for Request and Response ---
class ResumeAnalysisRequest(BaseModel):
    """
    Request model for resume analysis.
    For now, accepts raw text. File uploads can be added later.
    """

    resume_text: str = Field(..., description="The full text of the resume.")
    job_description_text: str = Field(
        ..., description="The full text of the job description."
    )


class FeedbackComponent(BaseModel):
    """
    A single piece of feedback.
    (This is a generic component, the actual feedback structure from feedback_generator is a dict of lists of strings)
    For the mock, we'll simplify. The actual integration will use the richer structure.
    """

    category: str  # e.g., "overall_summary", "missing_keywords_suggestions", "strengths", "areas_for_improvement"
    messages: List[str]


class ResumeAnalysisResponse(BaseModel):
    """
    Response model for resume analysis.
    """

    overall_score: float = Field(..., example=75.5)
    semantic_similarity_score: float = Field(..., example=0.82)
    keyword_match_score: float = Field(..., example=0.65)

    # The feedback structure from feedback_generator.py is Dict[str, List[str]]
    # e.g., {"overall_summary": ["Excellent match!"], "missing_keywords_suggestions": ["Consider adding 'XYZ'"], ...}
    feedback: Dict[str, List[str]] = Field(
        ...,
        example={
            "overall_summary": ["Mock summary: Good match!"],
            "strengths": ["Mock strength: Strong experience in Python."],
            "areas_for_improvement": [
                "Mock suggestion: Highlight more project details."
            ],
            "missing_keywords_suggestions": [
                "Mock missing: Consider 'Cloud Technologies'."
            ],
        },
    )

    # Include extracted keywords in the response
    resume_keywords: List[str] = Field(
        default_factory=list, example=["python", "api", "django"]
    )
    jd_keywords: List[str] = Field(
        default_factory=list, example=["python", "api", "fastapi"]
    )


# --- FastAPI Application Instance ---
app = FastAPI(
    title="Resume Screening and Job Matching API",
    description="API for analyzing resumes against job descriptions.",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# --- Event Handlers for Logging Startup and Shutdown ---
@app.on_event("startup")
async def startup_event():
    # Use a dictionary for extra context in logs, including a placeholder for request_id
    extra_context = {"request_id": "N/A"}
    logger.info("Application startup complete.", extra=extra_context)


@app.on_event("shutdown")
async def shutdown_event():
    extra_context = {"request_id": "N/A"}
    logger.info("Application shutdown.", extra=extra_context)


# --- API Endpoints ---
# Define a maximum acceptable length for input texts
MAX_INPUT_LENGTH = 200000  # Approx 200KB, adjust as needed


@app.post("/analyze_resume/", response_model=ResumeAnalysisResponse)
async def analyze_resume(
    fastapi_req: FastAPIRequest, request: ResumeAnalysisRequest
):  # Added FastAPIRequest
    """
    Analyzes a resume against a job description.

    This endpoint takes the text of a resume and a job description, processes them through an NLP pipeline (currently mocked),
    and returns an analysis including a match score and actionable feedback.

    **Request Body:**
    - `resume_text` (str): The full text content of the resume.
    - `job_description_text` (str): The full text content of the job description.

    **Response:**
    - `overall_score` (float): The overall compatibility score between 0 and 100.
    - `semantic_similarity_score` (float): Score from 0 to 1 indicating semantic similarity.
    - `keyword_match_score` (float): Score from 0 to 1 indicating keyword overlap.
    - `feedback` (dict): Structured feedback with categories like 'overall_summary', 'strengths', 'areas_for_improvement', 'missing_keywords_suggestions'.
    """
    request_id = str(uuid.uuid4())
    log_extra = {"request_id": request_id}

    logger.info(f"Received request to /analyze_resume/", extra=log_extra)
    logger.debug(
        f"Resume text (first 100 chars): {request.resume_text[:100]}...",
        extra=log_extra,
    )
    logger.debug(
        f"JD text (first 100 chars): {request.job_description_text[:100]}...",
        extra=log_extra,
    )

    # --- Specific Error Handling ---
    # Check for critical model loading (example for sentence_model)
    if global_sentence_model is None:
        logger.error(
            "Semantic similarity model (sentence_model) is not loaded. Service unavailable.",
            extra=log_extra,
        )
        raise HTTPException(
            status_code=503,  # Service Unavailable
            detail=f"A critical component is currently unavailable. Please try again later. Request ID: {request_id}",
        )

    # Check for input length
    if (
        len(request.resume_text) > MAX_INPUT_LENGTH
        or len(request.job_description_text) > MAX_INPUT_LENGTH
    ):
        logger.warning(
            f"Input text exceeds maximum length of {MAX_INPUT_LENGTH} characters.",
            extra=log_extra,
        )
        raise HTTPException(
            status_code=413,  # Payload Too Large
            detail=f"Input text is too long. Maximum allowed length is {MAX_INPUT_LENGTH} characters per field. Request ID: {request_id}",
        )

    if not request.resume_text.strip() or not request.job_description_text.strip():
        logger.warning(
            "One or both input texts are empty or contain only whitespace.",
            extra=log_extra,
        )
        # Or, could return a 400 Bad Request if this is considered invalid input
        # For now, let the pipeline handle it, it should result in low scores / specific feedback

    # Import NLP modules (consider moving to top level if they don't have heavy init costs not already handled)
    from backend.text_processor import preprocess_text
    from backend.keyword_extractor import extract_keywords_tfidf

    # semantic_analyzer.calculate_semantic_similarity uses global_sentence_model
    from backend.semantic_analyzer import calculate_semantic_similarity
    from backend.scorer import calculate_overall_score, calculate_keyword_match_score
    from backend.feedback_generator import generate_feedback

    try:
        logger.debug("Starting NLP pipeline processing...", extra=log_extra)

        # 1. Preprocess texts
        processed_resume_text = preprocess_text(request.resume_text)
        processed_jd_text = preprocess_text(request.job_description_text)

        # 2. Extract keywords (using TF-IDF for this integration)
        # extract_keywords_tfidf expects a list of documents.
        # It returns a list of lists of keywords. We take the first element for single doc.
        resume_keywords_list = extract_keywords_tfidf(
            [processed_resume_text] if processed_resume_text else [""]
        )
        resume_keywords = resume_keywords_list[0] if resume_keywords_list else []

        jd_keywords_list = extract_keywords_tfidf(
            [processed_jd_text] if processed_jd_text else [""]
        )
        jd_keywords = jd_keywords_list[0] if jd_keywords_list else []

        # 3. Calculate semantic similarity (using original texts for richer context)
        # Ensure calculate_semantic_similarity handles empty strings or add checks
        semantic_sim_score = calculate_semantic_similarity(
            request.resume_text, request.job_description_text
        )

        # 4. Calculate overall score
        # The calculate_overall_score function internally calls calculate_keyword_match_score
        overall_score = calculate_overall_score(
            resume_keywords, jd_keywords, semantic_sim_score
        )

        # For the response, we also need the individual keyword_match_score
        keyword_match_score_value = calculate_keyword_match_score(
            resume_keywords, jd_keywords
        )

        # 5. Generate feedback
        feedback_data = generate_feedback(
            resume_keywords, jd_keywords, semantic_sim_score, overall_score
        )

        logger.info(f"Successfully completed analysis.", extra=log_extra)

        return ResumeAnalysisResponse(
            overall_score=overall_score,
            semantic_similarity_score=semantic_sim_score,
            keyword_match_score=keyword_match_score_value,
            feedback=feedback_data,
            resume_keywords=resume_keywords,
            jd_keywords=jd_keywords,
        )

    except HTTPException as http_exc:
        # Re-raise HTTPExceptions directly
        # Already logged if it's one of our custom ones above
        # If not, log it here.
        if http_exc.status_code not in [
            413,
            503,
        ]:  # Avoid re-logging specific handled cases above
            logger.error(
                f"HTTPException during analysis: {http_exc.status_code} - {http_exc.detail}",
                exc_info=True,
                extra=log_extra,
            )
        raise http_exc

    except Exception as e:
        # Log the exception details for debugging
        logger.error(
            f"Unexpected error during resume analysis pipeline: {str(e)}",
            exc_info=True,
            extra=log_extra,
        )
        raise HTTPException(
            status_code=500,  # Internal Server Error
            detail=f"An unexpected error occurred during the analysis process. Please try again later. Request ID: {request_id}",
        )


@app.post("/analyze_resume_files/", response_model=ResumeAnalysisResponse)
async def analyze_resume_files(
    fastapi_req: FastAPIRequest,
    resume_file: UploadFile = File(...),
    job_description_file: UploadFile = File(...),
):
    """
    Analyzes a resume file against a job description file.

    This endpoint takes resume and job description files, extracts their text content,
    processes them through an NLP pipeline, and returns an analysis.
    """
    request_id = str(uuid.uuid4())
    log_extra = {"request_id": request_id}

    logger.info(f"Received request to /analyze_resume_files/", extra=log_extra)
    logger.info(
        f"Resume file: {resume_file.filename}, JD file: {job_description_file.filename}",
        extra=log_extra,
    )

    # Import file parsers
    from backend.resume_parser import extract_text_from_file
    from backend.jd_parser import extract_text_from_file as extract_jd_text

    try:
        # Save uploaded files temporarily
        resume_temp = tempfile.NamedTemporaryFile(delete=False)
        jd_temp = tempfile.NamedTemporaryFile(delete=False)

        try:
            # Write content to temp files
            shutil.copyfileobj(resume_file.file, resume_temp)
            shutil.copyfileobj(job_description_file.file, jd_temp)

            # Close temp files
            resume_temp.close()
            jd_temp.close()

            # Extract text from files
            resume_text = extract_text_from_file(resume_temp.name, resume_file.filename)
            jd_text = extract_jd_text(jd_temp.name, job_description_file.filename)

            # Create a request object
            request = ResumeAnalysisRequest(
                resume_text=resume_text, job_description_text=jd_text
            )

            # Process the request using the existing analyze_resume function
            return await analyze_resume(fastapi_req, request)

        finally:
            # Clean up temp files
            os.unlink(resume_temp.name)
            os.unlink(jd_temp.name)

    except Exception as e:
        logger.error(
            f"Error processing uploaded files: {str(e)}", exc_info=True, extra=log_extra
        )
        raise HTTPException(
            status_code=500,
            detail=f"Error processing uploaded files: {str(e)}. Request ID: {request_id}",
        )


@app.get("/", include_in_schema=False)
async def root():
    return {
        "message": "Welcome to the Resume Analyzer API. Go to /docs for API documentation."
    }


# --- How to Run (Instructions) ---
# To run the FastAPI development server:
# 1. Navigate to the project's root directory (the one containing the 'backend' folder).
# 2. Ensure Uvicorn is installed: pip install uvicorn[standard]
# 3. Run the server from the project root directory using the command:
#    uvicorn backend.main:app --reload
#    - `backend.main`: Refers to the `main.py` file in the `backend` directory.
#    - `app`: Refers to the FastAPI instance `app = FastAPI()` in `main.py`.
#    - `--reload`: Enables auto-reloading when code changes (for development).
# 4. The API will typically be available at http://127.0.0.1:8000
# 5. Access the interactive API documentation (Swagger UI) at http://127.0.0.1:8000/docs
#    or ReDoc at http://127.0.0.1:8000/redoc
