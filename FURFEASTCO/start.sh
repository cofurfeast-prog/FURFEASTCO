#!/bin/sh

# Unbuffer logs for Cloud Run
export PYTHONUNBUFFERED=1

# Get PORT from environment or default to 8000
PORT=${PORT:-8000}

# Debug: Print all environment variables (except secrets)
echo "=== Starting on port: $PORT ==="
echo "DB_HOST: $DB_HOST"
echo "ALLOWED_HOSTS: $ALLOWED_HOSTS"
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "PYTHONPATH: $PYTHONPATH"

# Set Django settings module for production
export DJANGO_SETTINGS_MODULE=FURFEASTCO.production

# Ensure Python can find the Django project
export PYTHONPATH=/app:$PYTHONPATH

# Skip migrations for now to avoid database connection issues
echo "Skipping migrations to avoid database connection issues"

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn server with optimized settings for Cloud Run
exec gunicorn FURFEASTCO.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 300 --keep-alive 2 --max-requests 1000 --max-requests-jitter 50
