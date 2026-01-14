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

def debug_profile_pictures():
    print("=== PROFILE PICTURE DEBUG ===")
    
    # Get all users
    users = User.objects.all()
    print(f"Total users: {users.count()}")
    
    for user in users:
        print(f"\n--- User: {user.username} ({user.first_name} {user.last_name}) ---")
        print(f"Email: {user.email}")
        
        # Check if user has profile
        try:
            profile = user.profile
            print(f"Profile exists: YES")
            print(f"Profile ID: {profile.id}")
            print(f"Phone number: {profile.phone_number}")
            print(f"Profile picture field: {profile.profile_picture}")
            
            if profile.profile_picture:
                print(f"Profile picture name: {profile.profile_picture.name}")
                print(f"Profile picture URL: {profile.profile_picture.url}")
                
                # Check if file actually exists
                try:
                    file_path = profile.profile_picture.path
                    print(f"File path: {file_path}")
                    if os.path.exists(file_path):
                        print(f"File exists on disk: YES")
                        print(f"File size: {os.path.getsize(file_path)} bytes")
                    else:
                        print(f"File exists on disk: NO")
                except Exception as e:
                    print(f"Error checking file path: {e}")
            else:
                print(f"Profile picture: NOT SET")
                
        except UserProfile.DoesNotExist:
            print(f"Profile exists: NO")
            # Create profile for this user
            profile = UserProfile.objects.create(user=user)
            print(f"Created new profile with ID: {profile.id}")
        except Exception as e:
            print(f"Error accessing profile: {e}")
    
    print("\n=== MEDIA SETTINGS DEBUG ===")
    from django.conf import settings
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
    
    # Check media directory
    if os.path.exists(settings.MEDIA_ROOT):
        print(f"Media root exists: YES")
        profiles_dir = os.path.join(settings.MEDIA_ROOT, 'profiles')
        if os.path.exists(profiles_dir):
            print(f"Profiles directory exists: YES")
            files = os.listdir(profiles_dir)
            print(f"Files in profiles directory: {files}")
        else:
            print(f"Profiles directory exists: NO")
    else:
        print(f"Media root exists: NO")

if __name__ == "__main__":
    debug_profile_pictures()