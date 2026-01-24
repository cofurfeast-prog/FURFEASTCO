from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting
import os

class GoogleCloudMediaStorage(GoogleCloudStorage):
    """Google Cloud Storage for media files"""
    bucket_name = setting('GS_BUCKET_NAME')
    file_overwrite = False
    default_acl = 'publicRead'