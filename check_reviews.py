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

# Count reviews
review_count = Review.objects.count()
print(f"Total reviews in database: {review_count}")

if review_count > 0:
    print("\nReview details:")
    for review in Review.objects.select_related('user', 'product').all():
        print(f"- {review.user.first_name} {review.user.last_name}: {review.rating} stars for {review.product.name}")
        print(f"  Comment: {review.comment[:50]}...")
        print()
else:
    print("No reviews found in database.")
    print("\nLet's create some sample reviews...")
    
    # Get some products and users
    products = Product.objects.all()[:3]
    users = User.objects.filter(is_staff=False)[:3]
    
    if products.exists() and users.exists():
        sample_reviews = [
            {"rating": 5, "comment": "Amazing quality! My dog absolutely loves this food. Highly recommended for all pet parents."},
            {"rating": 4, "comment": "Great product with excellent nutritional value. My cat has been healthier since switching to this."},
            {"rating": 5, "comment": "Outstanding service and premium quality products. FurFeast never disappoints us and our pets."},
            {"rating": 4, "comment": "Very satisfied with the purchase. Fast delivery and my pet loves the taste of this food."},
            {"rating": 5, "comment": "Best pet food brand I've tried! My pets are more energetic and their coat looks shinier."},
            {"rating": 4, "comment": "Excellent value for money. The ingredients are natural and my pets digest it well."}
        ]
        
        for i, review_data in enumerate(sample_reviews):
            if i < len(products) and i < len(users):
                Review.objects.get_or_create(
                    product=products[i % len(products)],
                    user=users[i % len(users)],
                    defaults={
                        'rating': review_data['rating'],
                        'comment': review_data['comment']
                    }
                )
        
        print(f"Created sample reviews. New total: {Review.objects.count()}")
    else:
        print("No products or users found to create sample reviews.")