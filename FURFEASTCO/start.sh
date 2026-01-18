#!/bin/bash

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start Daphne server (for WebSocket support)
daphne -b 0.0.0.0 -p 8000 FURFEASTCO.asgi:application
