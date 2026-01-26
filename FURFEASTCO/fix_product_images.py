import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')
django.setup()

from furfeast.models import Product
from google.cloud import storage
from google.oauth2 import credentials as oauth2_credentials
import subprocess

def get_gcloud_credentials():
    result = subprocess.run(['gcloud.cmd', 'auth', 'print-access-token'], capture_output=True, text=True, check=True)
    return oauth2_credentials.Credentials(token=result.stdout.strip())

# Get GCS files
creds = get_gcloud_credentials()
client = storage.Client(credentials=creds, project='project-e66945a9-799e-4142-bd5')
bucket = client.bucket('furfeastco-media')
blobs = list(bucket.list_blobs(prefix='products/'))

print(f"Found {len(blobs)} images in GCS\n")

# Map product names to images
product_image_map = {
    'Cat candy ': 'biralo_candy',
    'Dog Churpi': 'images.jpeg',
    'Dog Toy': 'dog_toy',
    'Cat Bell': 'cat_bell',
    'Retractable Dog Leash': 'dog_leash',
    'Pedigree': 'pedigree',
    'Friksies': 'Friskies_Cat',
    'Cat Cradle ': 'hacker'
}

# Update products
for product in Product.objects.all():
    search_term = product_image_map.get(product.name)
    if not search_term:
        print(f"No mapping for: {product.name}")
        continue
    
    # Find matching blob
    matching_blob = None
    for blob in blobs:
        if search_term.lower() in blob.name.lower():
            matching_blob = blob
            break
    
    if matching_blob:
        product.image = matching_blob.name
        product.save()
        print(f"[OK] {product.name}: {matching_blob.name}")
    else:
        print(f"[FAIL] {product.name}: No match for '{search_term}'")

print("\nDone!")
