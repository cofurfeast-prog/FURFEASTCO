from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from furfeast.models import Order, Notification
from django.utils import timezone

class Command(BaseCommand):
    help = 'Test notification system by simulating order status changes'

    def handle(self, *args, **options):
        self.stdout.write('Testing notification system...\n')
        
        # Get the first order that exists
        try:
            order = Order.objects.filter(status__in=['pending', 'paid', 'processing']).first()
            if not order:
                self.stdout.write(self.style.ERROR('No orders found with status pending/paid/processing'))
                return
            
            user = order.user
            order_id = order.order_id
            
            # Count notifications before
            notifications_before = Notification.objects.filter(user=user).count()
            self.stdout.write(f'User: {user.username}')
            self.stdout.write(f'Order: {order_id}')
            self.stdout.write(f'Current status: {order.status}')
            self.stdout.write(f'Notifications before: {notifications_before}')
            
            # Change status to shipped
            order.status = 'shipped'
            order.tracking_number = 'TEST123456'
            order.courier_name = 'Test Courier'
            order.save()
            
            # Count notifications after
            notifications_after = Notification.objects.filter(user=user).count()
            latest_notification = Notification.objects.filter(user=user).order_by('-created_at').first()
            
            self.stdout.write(f'\nAfter marking as shipped:')
            self.stdout.write(f'Notifications after: {notifications_after}')
            
            if notifications_after > notifications_before:
                self.stdout.write(self.style.SUCCESS('✓ Notification created successfully!'))
                self.stdout.write(f'Latest notification: {latest_notification.title}')
                self.stdout.write(f'Message: {latest_notification.message}')
            else:
                self.stdout.write(self.style.ERROR('✗ No notification was created'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))