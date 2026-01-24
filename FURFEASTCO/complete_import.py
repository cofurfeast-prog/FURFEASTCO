#!/usr/bin/env python3
"""
Complete data import with required fields
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
from django.core.files.base import ContentFile

def import_complete_data():
    print("Loading complete data...")
    
    with open('supabase_export.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with transaction.atomic():
        # Import products with required fields
        print("Importing products...")
        for product_data in data['products']:
            product, created = Product.objects.get_or_create(
                id=product_data['id'],
                defaults={
                    'name': product_data['name'],
                    'slug': slugify(product_data['name']),
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'category': product_data['category'],
                    'stock': product_data['stock'],
                    'is_out_of_stock': product_data['is_out_of_stock'],
                    'is_bestseller': product_data['is_bestseller'],
                    'rating': product_data['rating'],
                    'created_at': product_data['created_at'],
                    'image': 'products/placeholder.jpg'  # Placeholder image
                }
            )
        
        # Import orders
        print("Importing orders...")
        for order_data in data['orders']:
            user = User.objects.get(id=order_data['user_id'])
            order, created = Order.objects.get_or_create(
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
        
        # Import order items
        print("Importing order items...")
        for item_data in data['order_items']:
            order = Order.objects.get(id=item_data['order_id'])
            product = Product.objects.get(id=item_data['product_id'])
            item, created = OrderItem.objects.get_or_create(
                id=item_data['id'],
                defaults={
                    'order': order,
                    'product': product,
                    'quantity': item_data['quantity'],
                    'price': item_data['price']
                }
            )
        
        # Import reviews
        print("Importing reviews...")
        for review_data in data['reviews']:
            product = Product.objects.get(id=review_data['product_id'])
            user = User.objects.get(id=review_data['user_id'])
            review, created = Review.objects.get_or_create(
                id=review_data['id'],
                defaults={
                    'product': product,
                    'user': user,
                    'rating': review_data['rating'],
                    'comment': review_data['comment'],
                    'created_at': review_data['created_at']
                }
            )
    
    print("Complete import finished!")
    print(f"Products: {Product.objects.count()}")
    print(f"Orders: {Order.objects.count()}")
    print(f"Order Items: {OrderItem.objects.count()}")
    print(f"Reviews: {Review.objects.count()}")

if __name__ == "__main__":
    import_complete_data()