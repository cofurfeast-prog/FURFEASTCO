from django.core.management.base import BaseCommand
from furfeast.models import Notification
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Check notifications in database'

    def handle(self, *args, **options):
        self.stdout.write('Checking notifications in database...\n')
        
        # Get all notifications
        notifications = Notification.objects.all().order_by('-created_at')
        
        self.stdout.write(f'Total notifications: {notifications.count()}')
        
        for notification in notifications[:10]:  # Show last 10
            self.stdout.write(f'User: {notification.user.username}')
            self.stdout.write(f'Title: {notification.title}')
            self.stdout.write(f'Message: {notification.message}')
            self.stdout.write(f'Read: {notification.is_read}')
            self.stdout.write(f'Created: {notification.created_at}')
            self.stdout.write('---')
        
        # Check specific user
        try:
            user = User.objects.get(username='rajeshilamion')
            user_notifications = user.notifications.all().order_by('-created_at')
            self.stdout.write(f'\nNotifications for rajeshilamion: {user_notifications.count()}')
            for n in user_notifications:
                self.stdout.write(f'- {n.title}: {n.message} (Read: {n.is_read})')
        except User.DoesNotExist:
            self.stdout.write('User rajeshilamion not found')