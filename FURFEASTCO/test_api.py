import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import RequestFactory
from furfeast.views import notifications_api

# Get first user
user = User.objects.first()
print(f"Testing API for user: {user.username}")

# Create fake request
factory = RequestFactory()
request = factory.get('/api/notifications/')
request.user = user

# Call the view
response = notifications_api(request)
print(f"\nAPI Response Status: {response.status_code}")
print(f"API Response Content: {response.content.decode()}")
