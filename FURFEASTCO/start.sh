#!/bin/sh

# Unbuffer logs for Cloud Run
export PYTHONUNBUFFERED=1

# Get PORT from environment or default to 8080
PORT=${PORT:-8080}

# Set Django settings module for production
export DJANGO_SETTINGS_MODULE=FURFEASTCO.production

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn server on the PORT specified by Google Cloud Run
exec gunicorn FURFEASTCO.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
