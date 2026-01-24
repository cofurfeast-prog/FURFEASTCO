#!/usr/bin/env python
"""
Test script to verify Google Cloud database connectivity and data retrieval
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.append(str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')

# Setup Django
django.setup()

def test_database_connection():
    """Test basic database connectivity"""
    print("Testing database connection...")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"SUCCESS: Database connected successfully!")
            print(f"PostgreSQL version: {version[0]}")
            return True
    except Exception as e:
        print(f"ERROR: Database connection failed: {e}")
        return False

def test_user_data_retrieval():
    """Test user-related data retrieval"""
    print("\nTesting user data retrieval...")
    try:
        from django.contrib.auth.models import User
        from furfeast.models import UserProfile, Order, Cart, Wishlist
        
        # Test User model
        user_count = User.objects.count()
        print(f"Total users: {user_count}")
        
        # Test UserProfile model
        profile_count = UserProfile.objects.count()
        print(f"User profiles: {profile_count}")
        
        # Test Order model
        order_count = Order.objects.count()
        print(f"Total orders: {order_count}")
        
        # Test Cart model
        cart_count = Cart.objects.count()
        print(f"Active carts: {cart_count}")
        
        # Test Wishlist model
        wishlist_count = Wishlist.objects.count()
        print(f"Wishlist items: {wishlist_count}")
        
        # Test recent user activity
        if user_count > 0:
            recent_users = User.objects.order_by('-date_joined')[:3]
            print(f"Recent users:")
            for user in recent_users:
                print(f"   - {user.username} ({user.email}) - joined {user.date_joined}")
        
        return True
    except Exception as e:
        print(f"ERROR: User data retrieval failed: {e}")
        return False

def test_product_data_retrieval():
    """Test product-related data retrieval"""
    print("\nTesting product data retrieval...")
    try:
        from furfeast.models import Product, Review, FlashSale
        
        # Test Product model
        product_count = Product.objects.count()
        print(f"Total products: {product_count}")
        
        # Test categories
        categories = Product.objects.values_list('category', flat=True).distinct()
        print(f"Product categories: {list(categories)}")
        
        # Test Reviews
        review_count = Review.objects.count()
        print(f"Total reviews: {review_count}")
        
        # Test Flash Sales
        flash_sale_count = FlashSale.objects.count()
        print(f"Flash sales: {flash_sale_count}")
        
        # Test recent products
        if product_count > 0:
            recent_products = Product.objects.order_by('-created_at')[:3]
            print(f"Recent products:")
            for product in recent_products:
                print(f"   - {product.name} (${product.price}) - {product.category}")
        
        return True
    except Exception as e:
        print(f"ERROR: Product data retrieval failed: {e}")
        return False

def test_google_cloud_storage():
    """Test Google Cloud Storage configuration"""
    print("\nTesting Google Cloud Storage configuration...")
    try:
        from django.conf import settings
        
        # Check GCS settings
        gs_bucket = getattr(settings, 'GS_BUCKET_NAME', None)
        gs_project = getattr(settings, 'GS_PROJECT_ID', None)
        gs_credentials = getattr(settings, 'GS_CREDENTIALS', None)
        
        print(f"GCS Bucket: {gs_bucket or 'Not configured'}")
        print(f"GCS Project ID: {gs_project or 'Not configured'}")
        print(f"GCS Credentials: {'Configured' if gs_credentials else 'Not configured'}")
        
        # Check storage backend
        storages = getattr(settings, 'STORAGES', {})
        default_storage = storages.get('default', {}).get('BACKEND', 'Not configured')
        print(f"Default storage backend: {default_storage}")
        
        return True
    except Exception as e:
        print(f"ERROR: GCS configuration check failed: {e}")
        return False

def test_environment_variables():
    """Test environment variables"""
    print("\nTesting environment variables...")
    try:
        import os
        
        # Database variables
        db_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_PORT']
        print("Database variables:")
        for var in db_vars:
            value = os.getenv(var)
            if var == 'DB_PASSWORD':
                print(f"   {var}: {'***' if value else 'Not set'}")
            else:
                print(f"   {var}: {value or 'Not set'}")
        
        # Google Cloud variables
        gcs_vars = ['GS_BUCKET_NAME', 'GS_PROJECT_ID', 'GOOGLE_APPLICATION_CREDENTIALS']
        print("\nGoogle Cloud variables:")
        for var in gcs_vars:
            value = os.getenv(var)
            print(f"   {var}: {value or 'Not set'}")
        
        return True
    except Exception as e:
        print(f"ERROR: Environment variables check failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Starting FurFeast Google Cloud Database Test")
    print("=" * 50)
    
    tests = [
        test_environment_variables,
        test_database_connection,
        test_user_data_retrieval,
        test_product_data_retrieval,
        test_google_cloud_storage,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"ERROR: Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"Passed: {sum(results)}/{len(results)}")
    print(f"Failed: {len(results) - sum(results)}/{len(results)}")
    
    if all(results):
        print("\nSUCCESS: All tests passed! Your Google Cloud setup is working correctly.")
    else:
        print("\nWARNING: Some tests failed. Please check the configuration.")
    
    return all(results)

if __name__ == "__main__":
    main()