from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from furfeast.models import Order, Notification
from django.utils import timezone

class Command(BaseCommand):
    help = 'Test notification creation when order status changes'
    
    def handle(self, *args, **options):
        # Find an order to test with
        order = Order.objects.filter(status__in=['pending', 'paid', 'processing']).first()
        
        if not order:
            self.stdout.write(self.style.ERROR('No testable orders found'))
            return
        
        # Count notifications before
        notifications_before = Notification.objects.filter(user=order.user).count()
        
        self.stdout.write(f'Testing with order: {order.order_id} for user: {order.user.username}')
        self.stdout.write(f'Current status: {order.status}')
        self.stdout.write(f'Notifications before: {notifications_before}')
        
        # Change status to delivered
        order.status = 'delivered'
        order.save()
        
        # Count notifications after
        notifications_after = Notification.objects.filter(user=order.user).count()
        latest_notification = Notification.objects.filter(user=order.user).order_by('-created_at').first()
        
        self.stdout.write(f'Notifications after: {notifications_after}')
        
        if notifications_after > notifications_before:
            self.stdout.write(self.style.SUCCESS('Notification created successfully!'))
            self.stdout.write(f'Title: {latest_notification.title}')
            self.stdout.write(f'Message: {latest_notification.message}')
        else:
            self.stdout.write(self.style.ERROR('No notification was created'))