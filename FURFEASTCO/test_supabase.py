import os
import sys
import django

# Add the project directory to Python path
sys.path.append('e:/FURFEASTCO/FURFEASTCO')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')
django.setup()

from django.conf import settings
from furfeast.storage import SupabaseStorage
from furfeast.models import HeroImage, Product

print("=== Supabase Connection Test ===")
print(f"SUPABASE_URL: {getattr(settings, 'SUPABASE_URL', 'NOT SET')}")
print(f"SUPABASE_KEY: {'SET' if getattr(settings, 'SUPABASE_KEY', None) else 'NOT SET'}")
print(f"SUPABASE_BUCKET_NAME: {getattr(settings, 'SUPABASE_BUCKET_NAME', 'NOT SET')}")

print("\n=== Testing Storage Class ===")
storage = SupabaseStorage()
print(f"Storage enabled: {getattr(storage, 'supabase_enabled', False)}")

print("\n=== Testing Hero Images ===")
hero_images = HeroImage.objects.all()[:3]
for hero in hero_images:
    print(f"Hero: {hero.title}")
    print(f"Image field: {hero.image}")
    print(f"Image name: {hero.image.name}")
    print(f"Generated URL: {hero.image.url}")
    print("---")

print("\n=== Testing Products ===")
products = Product.objects.all()[:3]
for product in products:
    print(f"Product: {product.name}")
    print(f"Image field: {product.image}")
    print(f"Image name: {product.image.name}")
    print(f"Generated URL: {product.image.url}")
    print("---")

print("\n=== Manual URL Test ===")
test_name = "hero/465755b5-c73e-462e-adf1-6049fe893789_wmremove-transformed.jpeg"
manual_url = storage.url(test_name)
print(f"Manual URL for {test_name}: {manual_url}")