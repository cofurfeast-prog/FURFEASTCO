import os
from .settings import *

# Override DEBUG setting
DEBUG = False

# Set ALLOWED_HOSTS for production
ALLOWED_HOSTS = ['furfeastco-168900719564.australia-southeast2.run.app', '.run.app', 'localhost', '127.0.0.1']

# CSRF settings for Cloud Run deployment
CSRF_TRUSTED_ORIGINS = [
    'https://furfeastco-168900719564.australia-southeast2.run.app',
    'https://*.australia-southeast2.run.app',
]

# Database configuration for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', 5432),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'OPTIONS': {
            'sslmode': 'require',
        },
        'CONN_MAX_AGE': 0,
        'CONN_HEALTH_CHECKS': True,
    }
}

# Override storage settings for production
STORAGES = {
    "default": {
        "BACKEND": "furfeast.storage.SupabaseStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Security settings for production
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Override secret key if provided
if os.environ.get('SECRET_KEY'):
    SECRET_KEY = os.environ.get('SECRET_KEY')

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