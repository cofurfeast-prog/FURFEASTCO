import os
from .settings import *

DEBUG = False
ALLOWED_HOSTS = [
    "furfeastco-h2mw7nen5q-km.a.run.app",
    "*.a.run.app",
    "localhost",
    "127.0.0.1",
]

# CSRF settings for Cloud Run deployment
CSRF_TRUSTED_ORIGINS = [
    'https://furfeastco-h2mw7nen5q-km.a.run.app',
    'https://*.a.run.app',
]

# Use environment variables with fallbacks
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('DB_USER', 'postgres.wivxshghrwmgxstaowjl'),
        'PASSWORD': os.environ.get('DB_PASSWORD', '301197997Mom@'),
        'HOST': os.environ.get('DB_HOST', 'aws-1-ap-northeast-2.pooler.supabase.com'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require',
            'connect_timeout': 10,
        },
        'CONN_MAX_AGE': 0,  # Disable persistent connections for stability
        'CONN_HEALTH_CHECKS': True,
    }
}

# Supabase Configuration with fallbacks
SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://wivxshghrwmgxstaowjl.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_SERVICE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndpdnhzaGdocndtZ3hzdGFvd2psIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NzE4NDU2MSwiZXhwIjoyMDgyNzYwNTYxfQ.F62rm6cFzBccK477VyqFVSjXCzCeW4ZmsTQ1LJYrOvY')
SUPABASE_BUCKET_NAME = 'FurfeastCo.'

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / 'furfeast' / 'static',
]

# Modern Storage Configuration (Django 4.2+)
STORAGES = {
    "default": {
        "BACKEND": "furfeast.storage.SupabaseStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Security settings for production
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Email Configuration with fallbacks
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'cofurfeast@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'omylzdzofbxymrxv')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Secret key with fallback
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-u%=m_jym@7l@45gval389byel^zg#%7pian(h3p0j68y90%+q+')

# Comprehensive logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}