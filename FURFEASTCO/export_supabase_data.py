#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export all data from current Supabase database
"""
import os
import sys
import django

# Set UTF-8 encoding for Windows
os.environ['PYTHONIOENCODING'] = 'utf-8'
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')
django.setup()

def export_all_data():
    """Export all data from current database"""
    print("Exporting all data from Supabase...")
    
    # Set UTF-8 encoding for Windows
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Export all furfeast app data with UTF-8 encoding
    os.system('python manage.py dumpdata furfeast --output=furfeast_data.json --indent=2')
    
    # Export users with UTF-8 encoding
    os.system('python manage.py dumpdata auth.User --output=auth_users.json --indent=2')
    
    # Export everything as backup with UTF-8 encoding
    os.system('python manage.py dumpdata --output=complete_backup.json --indent=2')
    
    print("✅ Data export completed!")
    print("Files created:")
    print("- furfeast_data.json (app data)")
    print("- auth_users.json (user accounts)")
    print("- complete_backup.json (full backup)")

if __name__ == "__main__":
    export_all_data()