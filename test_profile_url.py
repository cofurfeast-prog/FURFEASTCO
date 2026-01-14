#!/usr/bin/env python
import os
import sys
import django
import requests

# Add the project directory to the Python path
sys.path.append('e:\\FURFEASTCO\\FURFEASTCO')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')
django.setup()

from django.contrib.auth.models import User
from furfeast.models import UserProfile

def test_profile_urls():
    print("=== TESTING PROFILE PICTURE URLS ===")
    
    # Get user with profile picture
    user = User.objects.get(username='nishakatuwal.77')
    profile = user.profile
    
    print(f"User: {user.first_name} {user.last_name}")
    print(f"Profile picture field: {profile.profile_picture}")
    print(f"Profile picture name: {profile.profile_picture.name}")
    print(f"Profile picture URL: {profile.profile_picture.url}")
    
    # Test if URL is accessible
    try:
        response = requests.head(profile.profile_picture.url, timeout=10)
        print(f"URL Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'Unknown')}")
        if response.status_code == 200:
            print("URL is accessible")
        else:
            print("URL is not accessible")
    except Exception as e:
        print(f"Error accessing URL: {e}")
    
    # Test template logic
    print(f"\n=== TEMPLATE LOGIC TEST ===")
    print(f"user.profile exists: {hasattr(user, 'profile')}")
    print(f"user.profile: {user.profile}")
    print(f"user.profile.profile_picture: {user.profile.profile_picture}")
    print(f"bool(user.profile.profile_picture): {bool(user.profile.profile_picture)}")
    
    # Test the exact template condition
    if user.profile and user.profile.profile_picture:
        print("Template condition should show image")
        print(f"Image src would be: {user.profile.profile_picture.url}")
    else:
        print("Template condition would show initials")
        initials = f"{user.first_name[0].upper() if user.first_name else ''}{user.last_name[0].upper() if user.last_name else ''}"
        print(f"Initials would be: {initials}")

if __name__ == "__main__":
    test_profile_urls()