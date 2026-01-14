#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('e:\\FURFEASTCO\\FURFEASTCO')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')
django.setup()

from django.core.files.base import ContentFile
from furfeast.storage import SupabaseStorage
from django.conf import settings

def test_supabase_upload():
    print("=== TESTING SUPABASE UPLOAD ===")
    
    # Check configuration
    print(f"SUPABASE_URL: {settings.SUPABASE_URL}")
    print(f"SUPABASE_KEY: {'SET' if settings.SUPABASE_KEY else 'NOT SET'}")
    print(f"SUPABASE_BUCKET_NAME: {settings.SUPABASE_BUCKET_NAME}")
    
    # Create storage instance
    storage = SupabaseStorage()
    print(f"Storage enabled: {storage.supabase_enabled}")
    print(f"Storage key: {'SET' if storage.supabase_key else 'NOT SET'}")
    
    # Create a test file
    test_content = b"This is a test file for Supabase upload"
    test_file = ContentFile(test_content, name="test_upload.txt")
    
    print(f"\nTesting file upload...")
    try:
        # Save the file
        saved_name = storage._save("profiles/test_upload.txt", test_file)
        print(f"File saved as: {saved_name}")
        
        # Get the URL
        file_url = storage.url(saved_name)
        print(f"File URL: {file_url}")
        
        # Test if file exists
        exists = storage.exists(saved_name)
        print(f"File exists: {exists}")
        
        # Test file size
        size = storage.size(saved_name)
        print(f"File size: {size} bytes")
        
        # Test if URL is accessible
        import requests
        try:
            response = requests.head(file_url, timeout=10)
            print(f"URL accessible: {response.status_code == 200} (Status: {response.status_code})")
        except Exception as e:
            print(f"URL test error: {e}")
        
        # Clean up - delete the test file
        print(f"\nCleaning up...")
        storage.delete(saved_name)
        print(f"Test file deleted")
        
    except Exception as e:
        print(f"Upload test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_supabase_upload()