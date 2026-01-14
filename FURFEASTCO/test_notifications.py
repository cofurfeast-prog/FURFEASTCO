import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')
django.setup()

from django.contrib.auth.models import User
from furfeast.models import Notification
from django.utils import timezone

# Get first user
user = User.objects.first()
if not user:
    print("No users found!")
    exit()

print(f"Testing notifications for user: {user.username}")
print(f"Total notifications: {Notification.objects.filter(user=user).count()}")

# List all notifications
notifications = Notification.objects.filter(user=user).order_by('-created_at')[:10]
print("\nNotifications:")
for n in notifications:
    print(f"  ID: {n.id}")
    print(f"  Title: {n.title}")
    print(f"  Type: {n.notification_type}")
    print(f"  Read: {n.is_read}")
    print(f"  Created: {n.created_at}")
    print(f"  Link: {n.link}")
    print("  ---")

# Check unread count
unread = Notification.objects.filter(user=user, is_read=False).count()
print(f"\nUnread notifications: {unread}")

# Create test notification if none exist
if Notification.objects.filter(user=user).count() == 0:
    print("\nCreating test notification...")
    Notification.objects.create(
        user=user,
        title="Test Order Update",
        message="Your order has been shipped",
        notification_type="order",
        link="/profile/",
        is_read=False
    )
    print("Test notification created!")
