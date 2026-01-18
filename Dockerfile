FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY FURFEASTCO/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY FURFEASTCO/ .

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media

# Make start script executable
RUN chmod +x start.sh

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=FURFEASTCO.production
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Google Cloud Run uses PORT environment variable
EXPOSE $PORT

CMD ["./start.sh"]