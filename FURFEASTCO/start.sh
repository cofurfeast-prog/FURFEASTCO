#!/bin/sh

export PYTHONUNBUFFERED=1
PORT=${PORT:-8000}

echo "=== STARTING CLOUD RUN DEBUG ==="
echo "Working directory: $(pwd)"
echo "Files in FURFEASTCO directory:"
ls -la FURFEASTCO/ 2>/dev/null || echo "ERROR: FURFEASTCO directory not found!"

# Create temp_settings.py if it doesn't exist
if [ ! -f "FURFEASTCO/temp_settings.py" ]; then
    echo "Creating temp_settings.py..."
    cat > FURFEASTCO/temp_settings.py << 'EOF'
DEBUG = True
ALLOWED_HOSTS = ['*']
SECRET_KEY = 'temp-key-123'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/db.sqlite3',
    }
}
INSTALLED_APPS = ['django.contrib.staticfiles']
MIDDLEWARE = ['django.middleware.common.CommonMiddleware']
ROOT_URLCONF = 'FURFEASTCO.urls'
STATIC_URL = 'static/'
EOF
fi

# Create simple_urls.py if it doesn't exist
if [ ! -f "FURFEASTCO/simple_urls.py" ]; then
    echo "Creating simple_urls.py..."
    cat > FURFEASTCO/simple_urls.py << 'EOF'
from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>✅ App is running!</h1><p>Test successful.</p>")

def health(request):
    return HttpResponse("OK")

urlpatterns = [
    path('', home),
    path('health/', health),
]
EOF
fi

# Temporarily replace urls.py with simple version
if [ -f "FURFEASTCO/urls.py" ]; then
    cp FURFEASTCO/urls.py FURFEASTCO/urls.py.backup
    cp FURFEASTCO/simple_urls.py FURFEASTCO/urls.py
    echo "Using simple URL configuration"
fi

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
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.temp_settings')

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
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.temp_settings')

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

# Start Gunicorn
echo "🚀 Starting Gunicorn on port $PORT..."
exec gunicorn FURFEASTCO.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 300 \
    --access-logfile - \
    --error-logfile - \
    --log-level info