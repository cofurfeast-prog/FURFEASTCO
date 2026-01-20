#!/bin/sh

export PYTHONUNBUFFERED=1
PORT=${PORT:-8000}

echo "=== CLOUDRUN DEBUG MODE (NO DATABASE) ==="
echo "Starting on port: $PORT"
echo "Current directory: $(pwd)"
ls -la

# Use temporary settings without database
export DJANGO_SETTINGS_MODULE=FURFEASTCO.temp_settings

# Skip all database operations
echo "Skipping database operations..."

# Create a simple test view if it doesn't exist
cat > /tmp/test_view.py << 'EOF'
from django.http import HttpResponse
from django.urls import path

def home(request):
    return HttpResponse("""
    <h1>✅ FURFEASTCO is running on Cloud Run!</h1>
    <p>App is working without database</p>
    <ul>
        <li><a href="/health/">Health Check</a></li>
        <li><a href="/test/">Test Page</a></li>
        <li><a href="/admin/">Admin (won't work without DB)</a></li>
    </ul>
    """)

def health_check(request):
    return HttpResponse("OK", status=200)

def test_view(request):
    return HttpResponse("Test page is working!")

# Create minimal URL patterns
urlpatterns = [
    path('', home, name='home'),
    path('health/', health_check, name='health_check'),
    path('test/', test_view, name='test'),
    path('admin/', home, name='admin_placeholder'),
]
EOF

# Temporarily replace your urls.py with a simple version
if [ -f "FURFEASTCO/urls.py" ]; then
    cp FURFEASTCO/urls.py FURFEASTCO/urls.py.backup
    cat /tmp/test_view.py > FURFEASTCO/urls.py
    echo "Using temporary URL configuration"
fi

# Collect static files (skip if fails)
python manage.py collectstatic --noinput 2>/dev/null || echo "Collectstatic skipped"

# Start Gunicorn with minimal settings
echo "🚀 Starting Gunicorn on port $PORT..."
exec gunicorn FURFEASTCO.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 300 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug