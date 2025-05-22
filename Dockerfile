# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install required packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY simplified_app.py .
COPY sample_resume.txt .
COPY sample_job_description.txt .

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

USER appuser

# Expose the port Streamlit runs on
EXPOSE 8501

# Define the command to run the Streamlit application
CMD ["streamlit", "run", "simplified_app.py", "--server.port", "8501", "--server.address", "0.0.0.0", "--server.headless", "true"]
