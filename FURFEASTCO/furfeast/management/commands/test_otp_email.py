from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Test OTP email sending'

    def handle(self, *args, **options):
        test_email = 'awsbuilder02@gmail.com'
        test_otp = '123456'
        
        try:
            self.stdout.write(f'Sending test OTP to {test_email}...')
            self.stdout.write(f'Using SMTP: {settings.EMAIL_HOST}:{settings.EMAIL_PORT}')
            self.stdout.write(f'From: {settings.DEFAULT_FROM_EMAIL}')
            
            send_mail(
                'Test OTP - FurFeast',
                f'Your test verification code is: {test_otp}\n\nThis is a test email.',
                settings.DEFAULT_FROM_EMAIL,
                [test_email],
                fail_silently=False,
            )
            
            self.stdout.write(self.style.SUCCESS(f'Email sent successfully to {test_email}'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send email: {str(e)}'))
