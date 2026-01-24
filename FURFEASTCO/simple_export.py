#!/usr/bin/env python3
"""
Export Supabase data for migration
"""
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')
django.setup()

from django.contrib.auth.models import User
from furfeast.models import UserProfile, Product, Order, OrderItem, Review

def export_data():
    print("Exporting data...")
    
    # Users
    users = []
    for user in User.objects.all():
        users.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'date_joined': user.date_joined.isoformat() if user.date_joined else None
        })
    
    # Profiles
    profiles = []
    for profile in UserProfile.objects.all():
        profiles.append({
            'id': profile.id,
            'user_id': profile.user.id,
            'phone_number': profile.phone_number,
            'address': profile.address,
            'city': profile.city,
            'postal_code': profile.postal_code,
            'country': profile.country,
            'email_verified': profile.email_verified
        })
    
    # Products
    products = []
    for product in Product.objects.all():
        products.append({
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': str(product.price),
            'category': product.category,
            'stock': product.stock,
            'is_out_of_stock': product.is_out_of_stock,
            'is_bestseller': product.is_bestseller,
            'rating': product.rating,
            'created_at': product.created_at.isoformat()
        })
    
    # Orders
    orders = []
    for order in Order.objects.all():
        orders.append({
            'id': order.id,
            'user_id': order.user.id,
            'order_id': order.order_id,
            'total_amount': str(order.total_amount),
            'status': order.status,
            'payment_status': order.payment_status,
            'created_at': order.created_at.isoformat(),
            'shipping_address': order.shipping_address
        })
    
    # Order Items
    order_items = []
    for item in OrderItem.objects.all():
        order_items.append({
            'id': item.id,
            'order_id': item.order.id,
            'product_id': item.product.id,
            'quantity': item.quantity,
            'price': str(item.price)
        })
    
    # Reviews
    reviews = []
    for review in Review.objects.all():
        reviews.append({
            'id': review.id,
            'product_id': review.product.id,
            'user_id': review.user.id,
            'rating': review.rating,
            'comment': review.comment,
            'created_at': review.created_at.isoformat()
        })
    
    data = {
        'users': users,
        'profiles': profiles,
        'products': products,
        'orders': orders,
        'order_items': order_items,
        'reviews': reviews
    }
    
    with open('supabase_export.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Exported {len(users)} users")
    print(f"Exported {len(profiles)} profiles")
    print(f"Exported {len(products)} products")
    print(f"Exported {len(orders)} orders")
    print(f"Exported {len(order_items)} order items")
    print(f"Exported {len(reviews)} reviews")
    print("Data saved to supabase_export.json")

if __name__ == "__main__":
    export_data()