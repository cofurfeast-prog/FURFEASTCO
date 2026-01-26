import os
import subprocess
from google.cloud import storage
from google.oauth2 import credentials as oauth2_credentials

def check_gcs_permissions():
    """Check GCS bucket permissions and credentials."""
    
    # Check environment variable
    creds_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    print(f"GOOGLE_APPLICATION_CREDENTIALS: {creds_path or 'NOT SET'}")
    
    # Check bucket name
    bucket_name = os.getenv('GS_BUCKET_NAME', 'furfeastco-media')
    print(f"GS_BUCKET_NAME: {bucket_name}")
    
    try:
        # Get credentials from gcloud CLI
        result = subprocess.run(
            ['gcloud.cmd', 'auth', 'print-access-token'],
            capture_output=True,
            text=True,
            check=True
        )
        access_token = result.stdout.strip()
        credentials = oauth2_credentials.Credentials(token=access_token)
        project = os.getenv('GS_PROJECT_ID', 'project-e66945a9-799e-4142-bd5')
        
        print(f"[OK] Got gcloud CLI credentials")
        print(f"  Project: {project}")
        
        # Initialize storage client
        client = storage.Client(credentials=credentials, project=project)
        
        # Try to access bucket
        bucket = client.bucket(bucket_name)
        
        # Test permissions
        print(f"\nTesting permissions on bucket: {bucket_name}")
        
        # Check if bucket exists and is accessible
        if bucket.exists():
            print(f"[OK] Bucket exists and is accessible")
        else:
            print(f"[FAIL] Bucket does not exist or is not accessible")
            return
        
        # Test Storage Object Viewer permissions
        permissions = [
            'storage.objects.list',
            'storage.objects.get',
        ]
        
        # Test Storage Object Creator permissions (for uploads)
        upload_permissions = [
            'storage.objects.create',
        ]
        
        print("\nChecking Storage Object Viewer permissions:")
        for perm in permissions:
            try:
                result = bucket.test_iam_permissions([perm])
                if perm in result:
                    print(f"  [OK] {perm}")
                else:
                    print(f"  [FAIL] {perm} - MISSING")
            except Exception as e:
                print(f"  [FAIL] {perm} - Error: {e}")
        
        print("\nChecking Storage Object Creator permissions (for uploads):")
        for perm in upload_permissions:
            try:
                result = bucket.test_iam_permissions([perm])
                if perm in result:
                    print(f"  [OK] {perm}")
                else:
                    print(f"  [FAIL] {perm} - MISSING")
            except Exception as e:
                print(f"  [FAIL] {perm} - Error: {e}")
        
        # Try to list objects
        print("\nTrying to list objects:")
        try:
            blobs = list(bucket.list_blobs(max_results=5))
            print(f"  [OK] Successfully listed {len(blobs)} objects")
            for blob in blobs[:3]:
                print(f"    - {blob.name}")
        except Exception as e:
            print(f"  [FAIL] Failed to list objects: {e}")
        
    except Exception as e:
        print(f"\n[FAIL] Error: {e}")
        print("\nMake sure you're authenticated with: gcloud auth login")

if __name__ == '__main__':
    check_gcs_permissions()
