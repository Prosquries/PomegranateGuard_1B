# Use an official lightweight Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# Set the working directory
WORKDIR /app

# Install system dependencies (needed for some AI libraries)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements first to leverage Docker cache
COPY app/requirements.txt .

# Install Python dependencies
# Using --no-cache-dir to save space
RUN pip install --no-cache-dir -r requirements.txt

# Copy the models and the app code
COPY model/ /app/model/
COPY app/ /app/

# Create necessary directories and set permissions
RUN mkdir -p /app/instance /app/static/uploads && \
    chmod -R 777 /app/instance /app/static/uploads

# Expose the port Flask runs on
EXPOSE 5000

# Start the application using Gunicorn (more stable for production)
# We use 1 worker and 2 threads to keep RAM usage under 2GB
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "2", "--timeout", "120", "app:app"]
