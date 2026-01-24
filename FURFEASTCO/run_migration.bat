@echo off
echo Starting Cloud SQL Proxy...
start "Cloud SQL Proxy" gcloud sql connect furfeast-db --user=furfeast-user --database=furfeast

echo Waiting for proxy to start...
timeout /t 10

echo Running migrations...
python manage.py migrate

echo Importing data...
python import_data.py

echo Migration completed!
pause