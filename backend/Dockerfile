# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Poetry (if used, not in this project)
    # POETRY_VERSION=1.7.1 \
    # POETRY_HOME="/opt/poetry" \
    # POETRY_VIRTUALENVS_CREATE=false \
    # POETRY_NO_INTERACTION=1 \
    # PATH="$POETRY_HOME/bin:$PATH"

# For NLTK and spaCy downloads
ENV NLTK_DATA=/usr/share/nltk_data \
    SPACY_DATA_DIR=/usr/share/spacy_models

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install system dependencies that might be needed by Python packages
# e.g., build-essential for some packages, libgomp1 for some ML libs
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential libgomp1 && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install PyTorch for CPU first, then the rest of requirements
# This helps ensure CPU-only version and can manage dependencies better.
# Note: The specific torch version should match what sentence-transformers expects or is compatible with.
# The version in requirements.txt (2.7.0) should be compatible.
# We will try to install torch with its CPU index first.
RUN pip install --index-url https://download.pytorch.org/whl/cpu torch==2.7.0+cpu
RUN pip install -r requirements.txt

# Download NLTK and spaCy resources
# Ensure these are the exact resources needed by your application to keep the image lean.
# The `nltk.downloader` in Python code will use NLTK_DATA path.
# `python -m nltk.downloader -d /usr/share/nltk_data punkt stopwords wordnet averaged_perceptron_tagger`
# `python -m spacy download en_core_web_sm --data-path /usr/share/spacy_models` -> this is old spacy v2 syntax
# For spaCy v3+, models are packages. `en_core_web_sm` is listed in requirements.txt if installed as package.
# If `en_core_web_sm` is not in requirements.txt, it needs to be downloaded.

# Let's assume NLTK resources are downloaded via code or that a separate script handles it if needed.
# For this Dockerfile, we'll ensure the common ones are present.
# punkt, stopwords, wordnet were used in text_processor.py
# averaged_perceptron_tagger might be needed by some NLTK functions implicitly.
RUN python -m nltk.downloader -d ${NLTK_DATA} punkt stopwords wordnet averaged_perceptron_tagger

# For spaCy, 'en_core_web_sm' is usually installed as a package via pip if it's in requirements.txt
# If it's not, then:
RUN python -m spacy download en_core_web_sm

# Let's ensure it's downloaded if not installed as a package.
# The `semantic_analyzer.py` tries to load `en_core_web_sm`.
# It's better to include it in requirements.txt or download it here.
# Adding a download step for spaCy model for robustness:
RUN python -m spacy download en_core_web_sm

# Copy the rest of the backend application code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the application
# The Uvicorn command in backend/main.py uses backend.main:app
# This assumes the WORKDIR is the project root, and 'backend' is a subdirectory.
# If WORKDIR is /app (and code is copied into /app), then it should be main:app
# The current structure copies ./backend/* into /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
