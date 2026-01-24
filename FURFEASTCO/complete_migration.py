#!/usr/bin/env python3
"""
Complete migration from Supabase to Google Cloud SQL
"""
import os
import time
import subprocess

def run_command(command):
    """Run shell command and return result"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def wait_for_instance():
    """Wait for SQL instance to be ready"""
    print("Waiting for Google Cloud SQL instance to be ready...")
    while True:
        success, stdout, stderr = run_command("gcloud sql instances describe furfeast-db --format=\"value(state)\"")
        if success and "RUNNABLE" in stdout:
            print("Instance is ready!")
            break
        print("Instance still creating... waiting 30 seconds")
        time.sleep(30)

def setup_database():
    """Create database and user"""
    print("Setting up database and user...")
    
    # Create database
    success, stdout, stderr = run_command("gcloud sql databases create furfeast --instance=furfeast-db")
    if not success:
        print(f"Database creation failed: {stderr}")
        return False
    
    # Create user
    success, stdout, stderr = run_command("gcloud sql users create furfeast-user --instance=furfeast-db --password=FurfeastDB2024!")
    if not success:
        print(f"User creation failed: {stderr}")
        return False
    
    print("Database and user created successfully!")
    return True

def update_env_file():
    """Update .env file with Google Cloud SQL settings"""
    print("Updating .env file...")
    
    # Get connection name
    success, connection_name, stderr = run_command("gcloud sql instances describe furfeast-db --format=\"value(connectionName)\"")
    if not success:
        print(f"Failed to get connection name: {stderr}")
        return False
    
    connection_name = connection_name.strip()
    
    env_content = f"""# Google Cloud SQL Database Configuration
DB_HOST=127.0.0.1
DB_NAME=furfeast
DB_USER=furfeast-user
DB_PASSWORD=FurfeastDB2024!
DB_PORT=5432
CLOUD_SQL_CONNECTION_NAME={connection_name}

# Google Cloud Storage Configuration
GS_BUCKET_NAME=furfeastco-media
GS_PROJECT_ID=project-e66945a9-799e-4142-bd5
GOOGLE_APPLICATION_CREDENTIALS=

# Django Settings
SECRET_KEY=django-insecure-u%=m_jym@7l@45gval389byel^zg#%7pian(h3p0j68y90%+q+
DEBUG=True

# Email Configuration
EMAIL_HOST_USER=cofurfeast@gmail.com
EMAIL_HOST_PASSWORD=omylzdzofbxymrxv
DEFAULT_FROM_EMAIL=cofurfeast@gmail.com
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("Environment file updated!")
    return True

def run_migrations():
    """Run Django migrations"""
    print("Running Django migrations...")
    success, stdout, stderr = run_command("python manage.py migrate")
    if not success:
        print(f"Migration failed: {stderr}")
        return False
    print("Migrations completed!")
    return True

def import_data():
    """Import exported data"""
    print("Importing data...")
    success, stdout, stderr = run_command("python import_data.py")
    if not success:
        print(f"Data import failed: {stderr}")
        return False
    print("Data imported successfully!")
    return True

def main():
    """Main migration process"""
    print("=== Supabase to Google Cloud SQL Migration ===")
    
    # Step 1: Wait for instance
    wait_for_instance()
    
    # Step 2: Setup database
    if not setup_database():
        print("Failed to setup database")
        return
    
    # Step 3: Update environment
    if not update_env_file():
        print("Failed to update environment")
        return
    
    # Step 4: Start Cloud SQL Proxy
    print("Starting Cloud SQL Proxy...")
    success, connection_name, stderr = run_command("gcloud sql instances describe furfeast-db --format=\"value(connectionName)\"")
    connection_name = connection_name.strip()
    
    print(f"Run this command in a separate terminal:")
    print(f"gcloud sql connect furfeast-db --user=furfeast-user")
    print("Or use Cloud SQL Proxy:")
    print(f"cloud_sql_proxy -instances={connection_name}=tcp:5432")
    
    input("Press Enter when Cloud SQL Proxy is running...")
    
    # Step 5: Run migrations
    if not run_migrations():
        print("Failed to run migrations")
        return
    
    # Step 6: Import data
    if not import_data():
        print("Failed to import data")
        return
    
    print("\n=== Migration Completed Successfully! ===")
    print("Your application is now using Google Cloud SQL")
    print("Remember to:")
    print("1. Update your production deployment settings")
    print("2. Test all functionality")
    print("3. Update any backup scripts")

if __name__ == "__main__":
    main()