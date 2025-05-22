# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the frontend application code
COPY . .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

USER appuser

# Expose the port Streamlit runs on
EXPOSE 8501

# Define the command to run the Streamlit application
# Ensure the server address is 0.0.0.0 to be accessible outside the container
# --server.enableCORS=false might be needed if requests come from different origins/ports,
# though for a simple setup, it might not be necessary immediately.
# --server.headless true is useful for running in non-interactive environments.
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0", "--server.headless", "true"]
