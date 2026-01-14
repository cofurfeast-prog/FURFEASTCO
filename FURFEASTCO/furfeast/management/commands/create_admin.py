from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create default admin user'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'adminfurfeastco@gmail.com', 'admin@furfeast321')
            self.stdout.write(self.style.SUCCESS('Admin user created: admin/admin@furfeast321'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))