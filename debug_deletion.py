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

def debug_profile_deletion():
    print("=== DEBUGGING PROFILE PICTURE DELETION ===")
    
    # Get the user
    user = User.objects.get(username='nishakatuwal.77')
    profile = user.profile
    
    print(f"User: {user.first_name} {user.last_name}")
    print(f"Profile picture field: {profile.profile_picture}")
    print(f"Profile picture name: {profile.profile_picture.name if profile.profile_picture else 'None'}")
    print(f"Profile picture bool: {bool(profile.profile_picture)}")
    
    if profile.profile_picture:
        print(f"Profile picture URL: {profile.profile_picture.url}")
        
        # Test the template condition
        print(f"\nTemplate condition test:")
        print(f"user.profile: {user.profile}")
        print(f"user.profile.profile_picture: {user.profile.profile_picture}")
        print(f"bool(user.profile.profile_picture): {bool(user.profile.profile_picture)}")
        print(f"Condition result: {user.profile and user.profile.profile_picture}")
        
        # Simulate deletion
        print(f"\nSimulating deletion...")
        print(f"Before deletion: {profile.profile_picture}")
        
        # Clear the field
        profile.profile_picture.delete(save=False)
        profile.profile_picture = None
        profile.save()
        
        print(f"After deletion: {profile.profile_picture}")
        print(f"Profile picture bool after deletion: {bool(profile.profile_picture)}")
        
        # Refresh from database
        profile.refresh_from_db()
        print(f"After refresh from DB: {profile.profile_picture}")
        print(f"Bool after refresh: {bool(profile.profile_picture)}")
        
    else:
        print("No profile picture to delete")

if __name__ == "__main__":
    debug_profile_deletion()