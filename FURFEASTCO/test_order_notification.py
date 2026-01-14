import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')
django.setup()

from django.contrib.auth.models import User
from furfeast.models import Order, Notification

# Get first user and their order
user = User.objects.first()
order = Order.objects.filter(user=user).first()

if not order:
    print("No orders found for user!")
    exit()

print(f"Testing order status notification for user: {user.username}")
print(f"Order ID: {order.order_id}")
print(f"Current status: {order.status}")

# Check notifications before
before_count = Notification.objects.filter(user=user).count()
print(f"\nNotifications before: {before_count}")

# Change order status to trigger notification
print("\nChanging order status to 'processing'...")
order.status = 'processing'
order.save()

# Check notifications after
after_count = Notification.objects.filter(user=user).count()
print(f"Notifications after: {after_count}")

if after_count > before_count:
    print("✓ Notification created successfully!")
    latest = Notification.objects.filter(user=user).order_by('-created_at').first()
    print(f"  Title: {latest.title}")
    print(f"  Message: {latest.message}")
    print(f"  Type: {latest.notification_type}")
else:
    print("✗ No notification created - signal handler not working!")
