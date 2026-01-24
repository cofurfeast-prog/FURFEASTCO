#!/usr/bin/env python3
"""
Import data to Google Cloud SQL
"""
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')
django.setup()

from django.contrib.auth.models import User
from furfeast.models import UserProfile, Product, Order, OrderItem, Review
from django.db import transaction

def import_data():
    print("Loading data from supabase_export.json...")
    
    with open('supabase_export.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with transaction.atomic():
        print("Importing users...")
        for user_data in data['users']:
            User.objects.get_or_create(
                id=user_data['id'],
                defaults={
                    'username': user_data['username'],
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_active': user_data['is_active'],
                    'is_staff': user_data['is_staff'],
                    'date_joined': user_data['date_joined']
                }
            )
        
        print("Importing user profiles...")
        for profile_data in data['profiles']:
            user = User.objects.get(id=profile_data['user_id'])
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'phone_number': profile_data['phone_number'],
                    'address': profile_data['address'],
                    'city': profile_data['city'],
                    'postal_code': profile_data['postal_code'],
                    'country': profile_data['country'],
                    'email_verified': profile_data['email_verified']
                }
            )
        
        print("Importing products...")
        for product_data in data['products']:
            Product.objects.get_or_create(
                id=product_data['id'],
                defaults={
                    'name': product_data['name'],
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'category': product_data['category'],
                    'stock': product_data['stock'],
                    'is_out_of_stock': product_data['is_out_of_stock'],
                    'is_bestseller': product_data['is_bestseller'],
                    'rating': product_data['rating'],
                    'created_at': product_data['created_at']
                }
            )
        
        print("Importing orders...")
        for order_data in data['orders']:
            user = User.objects.get(id=order_data['user_id'])
            Order.objects.get_or_create(
                id=order_data['id'],
                defaults={
                    'user': user,
                    'order_id': order_data['order_id'],
                    'total_amount': order_data['total_amount'],
                    'status': order_data['status'],
                    'payment_status': order_data['payment_status'],
                    'created_at': order_data['created_at'],
                    'shipping_address': order_data['shipping_address']
                }
            )
        
        print("Importing order items...")
        for item_data in data['order_items']:
            order = Order.objects.get(id=item_data['order_id'])
            product = Product.objects.get(id=item_data['product_id'])
            OrderItem.objects.get_or_create(
                id=item_data['id'],
                defaults={
                    'order': order,
                    'product': product,
                    'quantity': item_data['quantity'],
                    'price': item_data['price']
                }
            )
        
        print("Importing reviews...")
        for review_data in data['reviews']:
            product = Product.objects.get(id=review_data['product_id'])
            user = User.objects.get(id=review_data['user_id'])
            Review.objects.get_or_create(
                id=review_data['id'],
                defaults={
                    'product': product,
                    'user': user,
                    'rating': review_data['rating'],
                    'comment': review_data['comment'],
                    'created_at': review_data['created_at']
                }
            )
    
    print("Data import completed successfully!")
    print(f"Imported {len(data['users'])} users")
    print(f"Imported {len(data['profiles'])} profiles")
    print(f"Imported {len(data['products'])} products")
    print(f"Imported {len(data['orders'])} orders")
    print(f"Imported {len(data['order_items'])} order items")
    print(f"Imported {len(data['reviews'])} reviews")

if __name__ == "__main__":
    import_data()