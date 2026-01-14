@echo off
echo ========================================
echo FurFeast Deployment Troubleshooting
echo ========================================

echo.
echo Step 1: Checking Python and Django installation...
python --version
python -c "import django; print('Django version:', django.get_version())"

echo.
echo Step 2: Checking environment variables...
echo DJANGO_SETTINGS_MODULE=%DJANGO_SETTINGS_MODULE%
echo SECRET_KEY=%SECRET_KEY%
echo DB_HOST=%DB_HOST%
echo DB_NAME=%DB_NAME%
echo DB_USER=%DB_USER%
echo SUPABASE_URL=%SUPABASE_URL%

echo.
echo Step 3: Running health check...
python health_check.py

echo.
echo Step 4: Testing database connection...
python manage.py check --database default

echo.
echo Step 5: Checking migrations...
python manage.py showmigrations

echo.
echo Step 6: Running migrations...
python manage.py migrate --noinput

echo.
echo Step 7: Collecting static files...
python manage.py collectstatic --noinput --clear

echo.
echo Step 8: Testing server startup...
echo Starting Django development server for 10 seconds...
timeout /t 10 /nobreak > nul & python manage.py runserver 127.0.0.1:8000 --noreload &
timeout /t 15 > nul
taskkill /f /im python.exe > nul 2>&1

echo.
echo ========================================
echo Deployment check complete!
echo ========================================
pause