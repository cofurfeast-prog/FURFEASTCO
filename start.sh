#!/bin/sh
export PYTHONUNBUFFERED=1
PORT=${PORT:-8000}

echo "=== CLOUD RUN DEBUG ==="
echo "Working directory: $(pwd)"
ls -la

# Change to Django project directory
cd FURFEASTCO

echo "=== Django project directory ==="
ls -la
echo "=== Checking WSGI ==="
ls -la FURFEASTCO/

# Test Django settings
echo "=== Testing Django ==="
python -c "
import sys
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')

try:
    import django
    django.setup()
    print('✅ Django setup successful')
    
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print('✅ WSGI application created')
except Exception as e:
    print(f'❌ Django failed: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
"

# Install gunicorn
pip install gunicorn

# Start server with verbose logging
echo "🚀 Starting Gunicorn..."
exec gunicorn FURFEASTCO.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 300 \
    --log-level debug \
    --access-logfile - \
    --error-logfile -
