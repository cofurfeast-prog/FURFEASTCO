#!/bin/bash
set -e

echo "Starting FurFeast deployment..."

# Create necessary directories
mkdir -p /app/staticfiles
mkdir -p /app/media

# Run health check first
echo "Running health check..."
python health_check.py || {
    echo "Health check failed, but continuing..."
}

echo "Running migrations..."
python manage.py migrate --noinput || {
    echo "Migration failed, exiting..."
    exit 1
}

echo "Creating superuser if needed..."
python manage.py shell -c "
try:
    from django.contrib.auth.models import User
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser('admin', 'admin@furfeast.com', 'admin123')
        print('Superuser created: admin/admin123')
    else:
        print('Superuser already exists')
except Exception as e:
    print(f'Error creating superuser: {e}')
"

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || {
    echo "Static files collection failed, but continuing..."
}

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000