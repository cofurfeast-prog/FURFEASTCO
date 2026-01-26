"""
Django management command to cleanup old messages and notifications
Run: python manage.py cleanup_old_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from furfeast.models import CustomerMessage, Notification


class Command(BaseCommand):
    help = 'Delete messages and notifications older than 30 days'

    def handle(self, *args, **options):
        # Calculate cutoff date (30 days ago)
        cutoff_date = timezone.now() - timedelta(days=30)
        
        self.stdout.write(self.style.WARNING(f'Deleting data older than: {cutoff_date}'))
        
        # Delete old chat messages (including images)
        old_messages = CustomerMessage.objects.filter(created_at__lt=cutoff_date)
        message_count = old_messages.count()
        for msg in old_messages:
            if msg.image:
                msg.image.delete(save=False)
        old_messages.delete()
        
        # Delete old notifications
        old_notifications = Notification.objects.filter(created_at__lt=cutoff_date)
        notification_count = old_notifications.count()
        old_notifications.delete()
        
        # Summary
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {message_count} old messages'))
        self.stdout.write(self.style.SUCCESS(f'✅ Deleted {notification_count} old notifications'))
        self.stdout.write(self.style.SUCCESS('Cleanup completed successfully!'))
