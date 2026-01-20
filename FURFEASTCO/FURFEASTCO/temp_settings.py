"""
Temporary settings for Cloud Run debugging
"""
import os

# Basic Django settings
DEBUG = True
ALLOWED_HOSTS = ['*']
SECRET_KEY = 'temporary-secret-key-for-cloud-run-12345'

# Database - Simple SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/db.sqlite3',
    }
}

# Minimal apps
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
]

# Minimal middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# URLs
ROOT_URLCONF = 'FURFEASTCO.urls'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATIC_ROOT = '/app/staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'