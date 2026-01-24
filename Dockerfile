FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY FURFEASTCO/ .

# Copy start script from parent
COPY start_simple.sh .

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media

# Make start script executable
RUN chmod +x start_simple.sh

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=FURFEASTCO.settings
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Expose port
EXPOSE 8080

CMD ["./start_simple.sh"]