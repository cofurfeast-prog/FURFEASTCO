#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('e:\\FURFEASTCO\\FURFEASTCO')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')
django.setup()

from furfeast.models import Review, User, Product

# Get products and users
products = list(Product.objects.all())
users = list(User.objects.filter(is_staff=False))

print(f"Found {len(products)} products and {len(users)} users")

if len(products) > 0 and len(users) > 0:
    sample_reviews = [
        {"rating": 5, "comment": "Amazing quality! My dog absolutely loves this food. Highly recommended for all pet parents."},
        {"rating": 4, "comment": "Great product with excellent nutritional value. My cat has been healthier since switching to this."},
        {"rating": 5, "comment": "Outstanding service and premium quality products. FurFeast never disappoints us and our pets."},
        {"rating": 4, "comment": "Very satisfied with the purchase. Fast delivery and my pet loves the taste of this food."},
        {"rating": 5, "comment": "Best pet food brand I've tried! My pets are more energetic and their coat looks shinier."},
        {"rating": 4, "comment": "Excellent value for money. The ingredients are natural and my pets digest it well."},
        {"rating": 5, "comment": "My dog's favorite! He gets so excited when he sees the FurFeast bag. Quality is top-notch."},
        {"rating": 4, "comment": "Good product overall. My cat is picky but she actually enjoys this food. Will order again."}
    ]
    
    created_count = 0
    for i, review_data in enumerate(sample_reviews):
        product = products[i % len(products)]
        user = users[i % len(users)]
        
        # Check if review already exists
        if not Review.objects.filter(product=product, user=user).exists():
            Review.objects.create(
                product=product,
                user=user,
                rating=review_data['rating'],
                comment=review_data['comment']
            )
            created_count += 1
            print(f"Created review: {user.first_name} -> {product.name} ({review_data['rating']} stars)")
    
    print(f"\nCreated {created_count} new reviews")
    print(f"Total reviews now: {Review.objects.count()}")
else:
    print("No products or users found to create reviews")