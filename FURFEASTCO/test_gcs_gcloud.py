import os
import subprocess
from google.cloud import storage
from google.oauth2 import credentials as oauth2_credentials
from google.auth import _cloud_sdk

def get_gcloud_credentials():
    """Get credentials from gcloud CLI."""
    try:
        # Get access token from gcloud
        result = subprocess.run(
            ['gcloud.cmd', 'auth', 'print-access-token'],
            capture_output=True,
            text=True,
            check=True
        )
        access_token = result.stdout.strip()
        
        # Create credentials object
        creds = oauth2_credentials.Credentials(token=access_token)
        return creds
    except Exception as e:
        print(f"Error getting gcloud credentials: {e}")
        return None

def test_gcs_with_gcloud():
    """Test GCS access using gcloud credentials."""
    bucket_name = os.getenv('GS_BUCKET_NAME', 'furfeastco-media')
    project_id = os.getenv('GS_PROJECT_ID', 'project-e66945a9-799e-4142-bd5')
    
    print(f"Testing GCS access with gcloud user credentials")
    print(f"Bucket: {bucket_name}")
    print(f"Project: {project_id}\n")
    
    creds = get_gcloud_credentials()
    if not creds:
        print("[FAIL] Could not get gcloud credentials")
        return
    
    print("[OK] Got gcloud credentials")
    
    try:
        # Create storage client
        client = storage.Client(credentials=creds, project=project_id)
        bucket = client.bucket(bucket_name)
        
        # Test bucket access
        if bucket.exists():
            print(f"[OK] Bucket exists and is accessible\n")
        else:
            print(f"[FAIL] Bucket not accessible\n")
            return
        
        # Test listing objects
        print("Testing object listing:")
        blobs = list(bucket.list_blobs(max_results=5))
        print(f"[OK] Listed {len(blobs)} objects")
        for blob in blobs[:3]:
            print(f"  - {blob.name}")
        
        print("\n[SUCCESS] GCS access working with gcloud credentials!")
        print("\nFor Django to use this, you need to:")
        print("1. Keep gcloud CLI authenticated: gcloud auth login")
        print("2. Django will use gcloud credentials automatically")
        
    except Exception as e:
        print(f"[FAIL] Error: {e}")

if __name__ == '__main__':
    test_gcs_with_gcloud()
