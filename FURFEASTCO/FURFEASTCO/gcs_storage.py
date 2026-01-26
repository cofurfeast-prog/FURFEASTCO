import subprocess
import os
from storages.backends.gcloud import GoogleCloudStorage
from google.oauth2 import credentials as oauth2_credentials
from google.auth import default

class GCloudCLIStorage(GoogleCloudStorage):
    """GCS storage backend that uses gcloud CLI credentials locally, default in production."""
    
    def __init__(self, **settings):
        if not settings.get('credentials'):
            settings['credentials'] = self._get_credentials()
        super().__init__(**settings)
    
    def _get_credentials(self):
        """Get credentials from gcloud CLI (local) or default (production)."""
        # Check if running in Cloud Run
        if os.getenv('K_SERVICE'):
            # Production: use default credentials
            try:
                creds, _ = default()
                return creds
            except Exception:
                return None
        
        # Local: use gcloud CLI
        try:
            result = subprocess.run(
                ['gcloud.cmd', 'auth', 'print-access-token'],
                capture_output=True,
                text=True,
                check=True
            )
            access_token = result.stdout.strip()
            return oauth2_credentials.Credentials(token=access_token)
        except Exception:
            # Fallback to default credentials
            try:
                creds, _ = default()
                return creds
            except Exception:
                return None
