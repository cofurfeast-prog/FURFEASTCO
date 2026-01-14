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

def test_current_profile_picture():
    print("=== TESTING CURRENT PROFILE PICTURE ===")
    
    # Get the user
    user = User.objects.get(username='nishakatuwal.77')
    profile = user.profile
    
    print(f"User: {user.first_name} {user.last_name}")
    print(f"Profile picture: {profile.profile_picture}")
    print(f"Profile picture name: {profile.profile_picture.name}")
    print(f"Profile picture URL: {profile.profile_picture.url}")
    
    # Test if the URL works
    try:
        response = requests.head(profile.profile_picture.url, timeout=10)
        print(f"URL Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'Unknown')}")
        
        if response.status_code == 200:
            print("SUCCESS! Profile picture URL is working!")
            print("The profile picture should now be visible in the dashboard.")
        else:
            print(f"FAILED! URL returned status: {response.status_code}")
            
    except Exception as e:
        print(f"Error testing URL: {e}")

if __name__ == "__main__":
    test_current_profile_picture()