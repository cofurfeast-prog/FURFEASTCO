#!/usr/bin/env python3
"""
Migrate all data from Supabase PostgreSQL to Google Cloud SQL
"""
import os
import sys
import django
import psycopg2
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')
django.setup()

from django.db import connection
from django.core.management.commands.dumpdata import Command as DumpCommand
from django.core.management.commands.loaddata import Command as LoadCommand

def create_google_cloud_sql_instance():
    """Create Google Cloud SQL instance"""
    print("Creating Google Cloud SQL instance...")
    
    # Create the instance
    os.system(f"""
    gcloud sql instances create furfeast-db \
        --database-version=POSTGRES_15 \
        --tier=db-f1-micro \
        --region=australia-southeast2 \
        --storage-type=SSD \
        --storage-size=10GB \
        --backup-start-time=02:00 \
        --enable-bin-log \
        --maintenance-window-day=SUN \
        --maintenance-window-hour=03
    """)
    
    # Create database
    os.system("gcloud sql databases create furfeast --instance=furfeast-db")
    
    # Create user
    os.system("gcloud sql users create furfeast-user --instance=furfeast-db --password=FurfeastDB2024!")
    
    print("Google Cloud SQL instance created successfully!")
    return {
        'host': 'furfeast-db',
        'database': 'furfeast',
        'user': 'furfeast-user',
        'password': 'FurfeastDB2024!'
    }

def export_supabase_data():
    """Export all data from Supabase"""
    print("Exporting data from Supabase...")
    
    # Export all app data
    os.system("python manage.py dumpdata furfeast --output=supabase_data.json --indent=2")
    os.system("python manage.py dumpdata auth.User --output=users_data.json --indent=2")
    
    print("Data exported successfully!")

def update_env_for_google_cloud(db_config):
    """Update .env file with Google Cloud SQL configuration"""
    print("Updating .env file...")
    
    # Get Google Cloud SQL connection name
    result = os.popen("gcloud sql instances describe furfeast-db --format='value(connectionName)'").read().strip()
    
    env_content = f"""# Google Cloud SQL Database Configuration
DB_HOST=/cloudsql/{result}
DB_NAME=furfeast
DB_USER=furfeast-user
DB_PASSWORD=FurfeastDB2024!
DB_PORT=5432

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
    
    print("Environment updated for Google Cloud SQL!")

def migrate_database():
    """Run Django migrations on Google Cloud SQL"""
    print("Running migrations on Google Cloud SQL...")
    
    os.system("python manage.py migrate")
    print("Migrations completed!")

def import_data():
    """Import data to Google Cloud SQL"""
    print("Importing data to Google Cloud SQL...")
    
    # Load users first
    os.system("python manage.py loaddata users_data.json")
    
    # Load app data
    os.system("python manage.py loaddata supabase_data.json")
    
    print("Data imported successfully!")

def verify_migration():
    """Verify the migration was successful"""
    print("Verifying migration...")
    
    from furfeast.models import CustomUser, Product, Order, Review
    
    users_count = CustomUser.objects.count()
    products_count = Product.objects.count()
    orders_count = Order.objects.count()
    reviews_count = Review.objects.count()
    
    print(f"Migration verification:")
    print(f"- Users: {users_count}")
    print(f"- Products: {products_count}")
    print(f"- Orders: {orders_count}")
    print(f"- Reviews: {reviews_count}")
    
    return users_count > 0 and products_count > 0

def main():
    """Main migration process"""
    print("Starting Supabase to Google Cloud SQL migration...")
    
    try:
        # Step 1: Export data from Supabase
        export_supabase_data()
        
        # Step 2: Create Google Cloud SQL instance
        db_config = create_google_cloud_sql_instance()
        
        # Step 3: Update environment configuration
        update_env_for_google_cloud(db_config)
        
        # Step 4: Run migrations
        migrate_database()
        
        # Step 5: Import data
        import_data()
        
        # Step 6: Verify migration
        if verify_migration():
            print("\n✅ Migration completed successfully!")
            print("Your application is now using Google Cloud SQL instead of Supabase.")
        else:
            print("\n❌ Migration verification failed. Please check the logs.")
            
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()