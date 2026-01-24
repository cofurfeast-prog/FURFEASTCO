#!/bin/sh

cd /app

export PYTHONUNBUFFERED=1
export DJANGO_SETTINGS_MODULE=FURFEASTCO.settings
export PYTHONPATH=/app
PORT=${PORT:-8080}

echo "Starting FURFEASTCO Production on port $PORT"

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

exec gunicorn FURFEASTCO.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info