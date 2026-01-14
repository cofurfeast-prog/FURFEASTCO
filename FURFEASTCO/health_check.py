#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.production')

# Setup Django
django.setup()

def check_database():
    """Test database connectivity"""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("✅ Database connection: OK")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_static_files():
    """Check if static files are configured correctly"""
    try:
        from django.contrib.staticfiles.finders import find
        from django.conf import settings
        
        print(f"📁 STATIC_ROOT: {settings.STATIC_ROOT}")
        print(f"📁 STATIC_URL: {settings.STATIC_URL}")
        print(f"📁 STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
        
        # Try to find a common static file
        css_file = find('css/styles.css')
        if css_file:
            print("✅ Static files: Found CSS file")
        else:
            print("⚠️  Static files: CSS file not found")
        return True
    except Exception as e:
        print(f"❌ Static files check failed: {e}")
        return False

def check_environment_variables():
    """Check critical environment variables"""
    required_vars = [
        'SECRET_KEY', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 
        'DB_HOST', 'SUPABASE_URL', 'SUPABASE_SERVICE_KEY'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.environ.get(var)
        if not value:
            missing_vars.append(var)
        else:
            print(f"✅ {var}: Set")
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    return True

def main():
    print("🔍 FurFeast Health Check")
    print("=" * 40)
    
    checks = [
        ("Environment Variables", check_environment_variables),
        ("Database Connection", check_database),
        ("Static Files", check_static_files),
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✅ All checks passed!")
        sys.exit(0)
    else:
        print("❌ Some checks failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()