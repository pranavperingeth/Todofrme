FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies (needed for psycopg2, yt-dlp, etc.)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY backend /app/backend

# Copy the frontend code
COPY frontend /app/frontend

# Expose port
EXPOSE 8080

# Command to run the application
# Use the PORT environment variable provided by Fly.io
CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port 8080"]
