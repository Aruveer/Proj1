# Dockerfile content to be created and uploaded
# Use a Python base image for running the FastAPI application
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
# We use the '--no-cache-dir' flag for clean, efficient builds
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code files
COPY main.py .
COPY github_utils.py .

# Command to run your FastAPI application using Uvicorn
# Hugging Face Spaces expects the app to run on port 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
