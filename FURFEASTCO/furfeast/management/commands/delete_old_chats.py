from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from furfeast.models import CustomerMessage

class Command(BaseCommand):
    help = 'Delete chat messages older than 30 days'

    def handle(self, *args, **kwargs):
        # Calculate the date 30 days ago
        thirty_days_ago = timezone.now() - timedelta(days=30)
        
        # Delete old messages
        deleted_count, _ = CustomerMessage.objects.filter(
            created_at__lt=thirty_days_ago
        ).delete()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {deleted_count} chat messages older than 30 days')
        )
