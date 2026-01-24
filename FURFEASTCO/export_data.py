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
from furfeast.models import (
    UserProfile, Product, Order, OrderItem, Review, Cart, CartItem,
    Wishlist, Blog, FlashSale, PromoCode, Notification, ChatRoom,
    CustomerMessage, FurFeastFamily, ContactMessage, AboutUs, HeroImage
)

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
    
    # Export user profiles
    profiles_data = []
    for profile in UserProfile.objects.all():
        profiles_data.append({
            'id': profile.id,
            'user_id': profile.user.id if profile.user else None,
            'phone_number': profile.phone_number,
            'address': profile.address,
            'city': profile.city,
            'postal_code': profile.postal_code,
            'country': profile.country,
            'email_verified': profile.email_verified
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
            'stock': product.stock,
            'is_out_of_stock': product.is_out_of_stock,
            'is_bestseller': product.is_bestseller,
            'rating': product.rating,
            'created_at': product.created_at.isoformat() if product.created_at else None
        })
    
    # Export orders
    orders_data = []
    for order in Order.objects.all():
        orders_data.append({
            'id': order.id,
            'user_id': order.user.id if order.user else None,
            'order_id': order.order_id,
            'total_amount': str(order.total_amount),
            'status': order.status,
            'payment_status': order.payment_status,
            'created_at': order.created_at.isoformat() if order.created_at else None,
            'shipping_address': order.shipping_address
        })
    
    # Export order items
    order_items_data = []
    for item in OrderItem.objects.all():
        order_items_data.append({
            'id': item.id,
            'order_id': item.order.id if item.order else None,
            'product_id': item.product.id if item.product else None,
            'quantity': item.quantity,
            'price': str(item.price)
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
        'profiles': profiles_data,
        'products': products_data,
        'orders': orders_data,
        'order_items': order_items_data,
        'reviews': reviews_data
    }
    
    with open('migration_data.json', 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Exported {len(users_data)} users")
    print(f"✅ Exported {len(profiles_data)} user profiles")
    print(f"✅ Exported {len(products_data)} products")
    print(f"✅ Exported {len(orders_data)} orders")
    print(f"✅ Exported {len(order_items_data)} order items")
    print(f"✅ Exported {len(reviews_data)} reviews")
    print("Data saved to migration_data.json")

if __name__ == "__main__":
    safe_export()