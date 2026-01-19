#!/bin/sh

# Unbuffer logs for Cloud Run
export PYTHONUNBUFFERED=1

# Get PORT from environment or default to 8080
PORT=${PORT:-8080}

# Set Django settings module for production
export DJANGO_SETTINGS_MODULE=FURFEASTCO.production

# Test database connection before running migrations
echo "Testing database connection..."
python -c "import os; import psycopg2; conn = psycopg2.connect(host=os.environ.get('DB_HOST'), database=os.environ.get('DB_NAME'), user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASSWORD'), port=os.environ.get('DB_PORT')); print('Database connection successful'); conn.close()"

if [ $? -eq 0 ]; then
    echo "Database connection verified, running migrations..."
    # Run migrations
    python manage.py migrate --noinput
else
    echo "Database connection failed, skipping migrations"
fi

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn server on the PORT specified by Google Cloud Run
exec gunicorn FURFEASTCO.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
