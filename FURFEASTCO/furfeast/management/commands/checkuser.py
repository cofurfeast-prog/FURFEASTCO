from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from furfeast.models import UserProfile, PendingRegistration

class Command(BaseCommand):
    help = 'Check user account'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str)
        parser.add_argument('--fix', action='store_true')

    def handle(self, *args, **options):
        email = options['email']
        
        self.stdout.write("="*60)
        self.stdout.write(f"Checking: {email}")
        self.stdout.write("="*60)
        
        try:
            user = User.objects.get(email=email)
            self.stdout.write(self.style.SUCCESS(f"\n✅ USER FOUND"))
            self.stdout.write(f"Username: {user.username}")
            self.stdout.write(f"Email: {user.email}")
            self.stdout.write(f"Name: {user.first_name} {user.last_name}")
            self.stdout.write(f"Active: {user.is_active}")
            self.stdout.write(f"Joined: {user.date_joined}")
            
            try:
                profile = UserProfile.objects.get(user=user)
                self.stdout.write(f"\n✅ PROFILE: Phone={profile.phone_number}, Verified={profile.email_verified}")
            except UserProfile.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"\n⚠️  NO PROFILE"))
            
            if options['fix']:
                self.stdout.write(f"\n{'='*60}")
                self.stdout.write("FIXING...")
                fixed = []
                
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    fixed.append("Activated")
                
                profile, created = UserProfile.objects.get_or_create(user=user)
                if created:
                    fixed.append("Created profile")
                
                if not profile.email_verified:
                    profile.email_verified = True
                    profile.save()
                    fixed.append("Verified email")
                
                if fixed:
                    self.stdout.write(self.style.SUCCESS(f"\n✅ Fixed: {', '.join(fixed)}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"\n✅ No issues"))
                    
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"\n❌ USER NOT FOUND"))
            
            try:
                pending = PendingRegistration.objects.get(email=email)
                self.stdout.write(self.style.WARNING(f"\n⚠️  PENDING: {pending.first_name} {pending.last_name}"))
                self.stdout.write(f"Check email for verification")
            except PendingRegistration.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"\n❌ NEVER REGISTERED - Sign up first"))
        
        self.stdout.write("\n" + "="*60)
