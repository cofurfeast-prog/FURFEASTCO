#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('e:\\FURFEASTCO\\FURFEASTCO')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')
django.setup()

from django.contrib.auth.models import User
from furfeast.models import UserProfile
from django.core.files.base import ContentFile
import requests

def test_profile_picture_upload():
    print("=== TESTING PROFILE PICTURE UPLOAD ===")
    
    # Get the user
    user = User.objects.get(username='nishakatuwal.77')
    profile = user.profile
    
    print(f"User: {user.first_name} {user.last_name}")
    print(f"Current profile picture: {profile.profile_picture}")
    
    # Download a test image from the internet
    print(f"\nDownloading test image...")
    try:\n        # Use a small test image\n        image_url = \"https://via.placeholder.com/150x150/FF6B35/FFFFFF?text=NK\"\n        response = requests.get(image_url, timeout=10)\n        \n        if response.status_code == 200:\n            print(f\"Downloaded image ({len(response.content)} bytes)\")\n            \n            # Create a ContentFile\n            image_file = ContentFile(response.content, name=\"test_profile.png\")\n            \n            # Save the profile picture\n            print(f\"Uploading to Supabase...\")\n            profile.profile_picture = image_file\n            profile.save()\n            \n            print(f\"Profile picture saved!\")\n            print(f\"New profile picture: {profile.profile_picture}\")\n            print(f\"Profile picture URL: {profile.profile_picture.url}\")\n            \n            # Test if the URL works\n            test_response = requests.head(profile.profile_picture.url, timeout=10)\n            print(f\"URL accessible: {test_response.status_code == 200} (Status: {test_response.status_code})\")\n            \n            if test_response.status_code == 200:\n                print(\"SUCCESS! Profile picture is now working with Supabase!\")\n            else:\n                print(f\"URL test failed: {test_response.status_code}\")\n                \n        else:\n            print(f\"Failed to download test image: {response.status_code}\")\n            \n    except Exception as e:\n        print(f\"Error: {e}\")\n        import traceback\n        traceback.print_exc()\n\nif __name__ == \"__main__\":\n    test_profile_picture_upload()