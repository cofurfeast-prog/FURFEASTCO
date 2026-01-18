#!/bin/bash

# Get PORT from environment or default to 8000
PORT=${PORT:-8000}

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start Daphne server on the PORT specified by Google Cloud Run
daphne -b 0.0.0.0 -p $PORT FURFEASTCO.asgi:application
