import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')
django.setup()

from django.contrib.auth.models import User
from furfeast.models import Notification

user = User.objects.first()
print(f"Testing Clear All for user: {user.username}\n")

# Show current state
print("BEFORE Clear All:")
notifications = Notification.objects.filter(user=user).order_by('-created_at')
for n in notifications:
    print(f"  [{n.notification_type}] {n.title} - Read: {n.is_read}")

print(f"\nTotal: {notifications.count()}")

# Simulate Clear All (delete all except unread messages)
from django.db.models import Q
deleted_count = Notification.objects.filter(user=user).exclude(
    Q(notification_type='message') & Q(is_read=False)
).delete()[0]

print(f"\nDeleted: {deleted_count} notifications")

# Show after state
print("\nAFTER Clear All:")
remaining = Notification.objects.filter(user=user).order_by('-created_at')
for n in remaining:
    print(f"  [{n.notification_type}] {n.title} - Read: {n.is_read}")

print(f"\nRemaining: {remaining.count()}")
print("\nExpected: Only unread messages should remain")
