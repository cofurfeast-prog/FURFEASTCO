#!/usr/bin/env python
"""
Fix existing product ratings
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('e:\\FURFEASTCO\\FURFEASTCO')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')
django.setup()

from furfeast.models import Review, Product
from django.db.models import Avg

def fix_product_ratings():
    print("=== FIXING PRODUCT RATINGS ===")
    
    # Get all products that have reviews
    products_with_reviews = Product.objects.filter(reviews__isnull=False).distinct()
    
    for product in products_with_reviews:
        reviews = Review.objects.filter(product=product)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        old_rating = product.rating
        
        product.rating = round(avg_rating, 1)
        product.save()
        
        print(f"Product: {product.name}")
        print(f"  Old rating: {old_rating}")
        print(f"  New rating: {product.rating}")
        print(f"  Reviews count: {reviews.count()}")
        print()
    
    print("Rating fix completed!")

if __name__ == "__main__":
    fix_product_ratings()