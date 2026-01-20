#!/bin/sh
export PYTHONUNBUFFERED=1
PORT=${PORT:-8000}

echo "=== CLOUD RUN TEST ==="
echo "Working directory: $(pwd)"
ls -la

# Change to Django project directory
cd FURFEASTCO

# Use existing settings
export DJANGO_SETTINGS_MODULE=FURFEASTCO.settings

# Install gunicorn
pip install gunicorn

# Start server
echo "Starting server on port $PORT..."
exec gunicorn FURFEASTCO.wsgi:application --bind 0.0.0.0:$PORT --workers 1
