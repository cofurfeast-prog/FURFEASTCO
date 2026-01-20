#!/bin/sh

export PYTHONUNBUFFERED=1
PORT=${PORT:-8080}

echo "=== STARTING FURFEASTCO ON CLOUD RUN ==="
echo "Working directory: $(pwd)"
echo "Files in FURFEASTCO directory:"
ls -la FURFEASTCO/ 2>/dev/null || echo "ERROR: FURFEASTCO directory not found!"

# Test Python/Django first
echo "=== Testing Python/Django ==="
python -c "
import sys
print(f'Python version: {sys.version}')

try:
    import django
    print(f'Django version: {django.__version__}')
except ImportError as e:
    print(f'ERROR: Cannot import Django: {e}')
    sys.exit(1)
"

# Test WSGI application
echo "=== Testing WSGI Application ==="
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.production')

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print('✅ WSGI application created successfully')
except Exception as e:
    print(f'❌ WSGI application failed: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"

# Test that the app actually works
echo "=== Testing Django Setup ==="
python -c "
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.production')

import django
django.setup()

from django.urls import get_resolver
try:
    resolver = get_resolver()
    print(f'✅ URL resolver loaded with {len(resolver.url_patterns)} patterns')
    
    # Test if we can resolve URLs
    match = resolver.resolve('/')
    print(f'✅ Root URL resolves to: {match.func.__name__}')
    
    match = resolver.resolve('/health/')
    print(f'✅ Health URL resolves to: {match.func.__name__}')
    
except Exception as e:
    print(f'❌ URL loading failed: {e}')
    import traceback
    traceback.print_exc()
"

# Run Django migrations
echo "=== Running Django migrations ==="
python manage.py migrate

# Collect static files
echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

# Start Gunicorn
echo "🚀 Starting Gunicorn on port $PORT..."
exec gunicorn FURFEASTCO.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 300 \
    --access-logfile - \
    --error-logfile - \
    --log-level info