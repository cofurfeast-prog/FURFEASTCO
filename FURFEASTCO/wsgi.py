import os
from django.core.wsgi import get_wsgi_application

# Use the same settings module your settings point at
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FURFEASTCO.settings')

application = get_wsgi_application()
