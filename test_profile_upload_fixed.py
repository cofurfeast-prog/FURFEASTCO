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
    print("Downloading test image...")
    try:
        # Use a small test image
        image_url = "https://via.placeholder.com/150x150/FF6B35/FFFFFF?text=NK"
        response = requests.get(image_url, timeout=10)
        
        if response.status_code == 200:
            print(f"Downloaded image ({len(response.content)} bytes)")
            
            # Create a ContentFile
            image_file = ContentFile(response.content, name="test_profile.png")
            
            # Save the profile picture
            print("Uploading to Supabase...")
            profile.profile_picture = image_file
            profile.save()
            
            print("Profile picture saved!")
            print(f"New profile picture: {profile.profile_picture}")
            print(f"Profile picture URL: {profile.profile_picture.url}")
            
            # Test if the URL works
            test_response = requests.head(profile.profile_picture.url, timeout=10)
            print(f"URL accessible: {test_response.status_code == 200} (Status: {test_response.status_code})")
            
            if test_response.status_code == 200:
                print("SUCCESS! Profile picture is now working with Supabase!")
            else:
                print(f"URL test failed: {test_response.status_code}")
                
        else:
            print(f"Failed to download test image: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_profile_picture_upload()