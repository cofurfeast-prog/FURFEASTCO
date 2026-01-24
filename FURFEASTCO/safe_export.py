#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manual data export from Supabase with Unicode handling
"""
import os
import sys
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')
django.setup()

from django.contrib.auth.models import User
from furfeast.models import *

def safe_export():
    """Export data with Unicode safety"""
    print("Exporting data safely...")
    
    # Export users
    users_data = []
    for user in User.objects.all():
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'date_joined': user.date_joined.isoformat() if user.date_joined else None
        })
    
    # Export custom users
    custom_users_data = []
    for user in CustomUser.objects.all():
        custom_users_data.append({
            'id': user.id,
            'user_id': user.user.id if user.user else None,
            'phone_number': user.phone_number,
            'address': user.address,
            'city': user.city,
            'postal_code': user.postal_code,
            'country': user.country,
            'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
            'is_email_verified': user.is_email_verified
        })
    
    # Export products
    products_data = []
    for product in Product.objects.all():
        products_data.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': str(product.price),
            'category': product.category,
            'stock_quantity': product.stock_quantity,
            'is_active': product.is_active,
            'created_at': product.created_at.isoformat() if product.created_at else None
        })
    
    # Export orders
    orders_data = []
    for order in Order.objects.all():
        orders_data.append({
            'id': order.id,
            'user_id': order.user.id if order.user else None,
            'total_amount': str(order.total_amount),
            'status': order.status,
            'created_at': order.created_at.isoformat() if order.created_at else None,
            'shipping_address': order.shipping_address
        })
    
    # Export reviews
    reviews_data = []
    for review in Review.objects.all():
        reviews_data.append({
            'id': review.id,
            'product_id': review.product.id if review.product else None,
            'user_id': review.user.id if review.user else None,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at.isoformat() if review.created_at else None
        })
    
    # Save all data
    export_data = {
        'users': users_data,
        'custom_users': custom_users_data,
        'products': products_data,
        'orders': orders_data,
        'reviews': reviews_data
    }
    
    with open('migration_data.json', 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Exported {len(users_data)} users")
    print(f"✅ Exported {len(custom_users_data)} custom users")
    print(f"✅ Exported {len(products_data)} products")
    print(f"✅ Exported {len(orders_data)} orders")
    print(f"✅ Exported {len(reviews_data)} reviews")
    print("Data saved to migration_data.json")

if __name__ == "__main__":
    safe_export()