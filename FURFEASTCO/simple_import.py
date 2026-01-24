#!/usr/bin/env python3
"""
Simple data import to Google Cloud SQL
"""
import os
import django
import json
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')
django.setup()

from django.contrib.auth.models import User
from furfeast.models import UserProfile, Product, Order, OrderItem, Review
from django.db import transaction

def import_data():
    print("Loading data...")
    
    with open('supabase_export.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with transaction.atomic():
        # Import users
        print("Importing users...")
        for user_data in data['users']:
            user, created = User.objects.get_or_create(
                id=user_data['id'],
                defaults={
                    'username': user_data['username'],
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_active': user_data['is_active'],
                    'is_staff': user_data['is_staff']
                }
            )
        
        # Import profiles
        print("Importing profiles...")
        for profile_data in data['profiles']:
            user = User.objects.get(id=profile_data['user_id'])
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'phone_number': profile_data.get('phone_number', ''),
                    'address': profile_data.get('address', ''),
                    'city': profile_data.get('city', ''),
                    'postal_code': profile_data.get('postal_code', ''),
                    'country': profile_data.get('country', 'Nepal'),
                    'email_verified': profile_data.get('email_verified', False)
                }
            )
        
        # Import products (skip for now due to required fields)
        print("Skipping products (missing required fields)...")
        
        # Import orders (skip for now)
        print("Skipping orders (depends on products)...")
        
        # Import reviews (skip for now)
        print("Skipping reviews (depends on products)...")
    
    print("Basic import completed!")
    print(f"Imported {len(data['users'])} users")
    print(f"Imported {len(data['profiles'])} profiles")

if __name__ == "__main__":
    import_data()