#!/usr/bin/env python
"""
Check review display on product pages
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('e:\\FURFEASTCO\\FURFEASTCO')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')
django.setup()

from furfeast.models import Review, Product, User
from django.db.models import Avg

def check_product_reviews():
    print("=== PRODUCT REVIEW DISPLAY CHECK ===")
    
    # Get the product with reviews
    pedigree = Product.objects.get(name="Pedigree")
    reviews = Review.objects.filter(product=pedigree).select_related('user').order_by('-created_at')
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    print(f"Product: {pedigree.name}")
    print(f"Current product rating: {pedigree.rating}")
    print(f"Calculated average rating: {avg_rating}")
    print(f"Number of reviews: {reviews.count()}")
    print()
    
    print("Reviews:")
    for review in reviews:
        print(f"- User: {review.user.first_name} {review.user.last_name}")
        print(f"  Username: {review.user.username}")
        print(f"  Rating: {review.rating}/5")
        print(f"  Comment: {review.comment}")
        print(f"  Date: {review.created_at}")
        print(f"  User has profile: {hasattr(review.user, 'profile')}")
        if hasattr(review.user, 'profile'):
            print(f"  Profile picture: {review.user.profile.profile_picture}")
        print()

if __name__ == "__main__":
    check_product_reviews()