import os
import requests
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.conf import settings
import uuid
import json

class SupabaseStorage(Storage):
    def __init__(self):
        self.supabase_enabled = True
        self.supabase_url = getattr(settings, 'SUPABASE_URL', 'https://wivxshghrwmgxstaowjl.supabase.co')
        self.supabase_key = getattr(settings, 'SUPABASE_KEY', '')
        self.bucket_name = getattr(settings, 'SUPABASE_BUCKET_NAME', 'FurfeastCo.')

    def url(self, name):
        if name and self.supabase_enabled:
            return f"{self.supabase_url}/storage/v1/object/public/{self.bucket_name}/{name}"
        return f"/media/{name}"

    def _save(self, name, content):
        # Generate unique filename
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)
        clean_name = f"{uuid.uuid4()}_{file_root}{file_ext}"
        final_path = os.path.join(dir_name, clean_name).replace('\\', '/')
        
        # Upload to Supabase
        if self.supabase_enabled and self.supabase_key:
            try:
                # Prepare the file content
                content.seek(0)  # Reset file pointer
                file_content = content.read()
                
                # Supabase storage upload URL
                upload_url = f"{self.supabase_url}/storage/v1/object/{self.bucket_name}/{final_path}"
                
                # Headers for Supabase API
                headers = {
                    'Authorization': f'Bearer {self.supabase_key}',
                    'Content-Type': 'application/octet-stream'
                }
                
                # Upload file to Supabase
                response = requests.post(upload_url, data=file_content, headers=headers, timeout=30)
                
                if response.status_code in [200, 201]:
                    print(f"Successfully uploaded {final_path} to Supabase")
                    return final_path
                else:
                    print(f"Supabase upload failed: {response.status_code} - {response.text}")
                    # Fall back to local storage
                    return self._save_locally(final_path, content, file_content)
                    
            except Exception as e:
                print(f"Error uploading to Supabase: {e}")
                # Fall back to local storage
                return self._save_locally(final_path, content, file_content)
        else:
            # Save locally if Supabase is not configured
            content.seek(0)
            file_content = content.read()
            return self._save_locally(final_path, content, file_content)
    
    def _save_locally(self, final_path, content, file_content=None):
        """Fallback method to save files locally"""
        local_path = os.path.join(settings.MEDIA_ROOT, final_path)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        if file_content:
            with open(local_path, 'wb') as f:
                f.write(file_content)
        else:
            content.seek(0)
            with open(local_path, 'wb') as f:
                for chunk in content.chunks():
                    f.write(chunk)
        
        print(f"Saved {final_path} locally as fallback")
        return final_path

    def _open(self, name, mode='rb'):
        # Try to open from local storage first
        local_path = os.path.join(settings.MEDIA_ROOT, name)
        if os.path.exists(local_path):
            return open(local_path, mode)
        
        # If not local, try to download from Supabase
        if self.supabase_enabled:
            try:
                url = self.url(name)
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    return ContentFile(response.content)
            except:
                pass
        
        raise FileNotFoundError(f"File {name} not found")

    def delete(self, name):
        # Delete from Supabase
        if self.supabase_enabled and self.supabase_key:
            try:
                delete_url = f"{self.supabase_url}/storage/v1/object/{self.bucket_name}/{name}"
                headers = {
                    'Authorization': f'Bearer {self.supabase_key}'
                }
                response = requests.delete(delete_url, headers=headers, timeout=10)
                if response.status_code == 200:
                    print(f"Deleted {name} from Supabase")
            except Exception as e:
                print(f"Error deleting from Supabase: {e}")
        
        # Delete from local storage
        local_path = os.path.join(settings.MEDIA_ROOT, name)
        if os.path.exists(local_path):
            os.remove(local_path)
            print(f"Deleted {name} locally")

    def exists(self, name):
        # Check Supabase first
        if self.supabase_enabled:
            try:
                url = self.url(name)
                response = requests.head(url, timeout=5)
                if response.status_code == 200:
                    return True
            except:
                pass
        
        # Check local storage
        local_path = os.path.join(settings.MEDIA_ROOT, name)
        return os.path.exists(local_path)

    def size(self, name):
        # Try local first
        local_path = os.path.join(settings.MEDIA_ROOT, name)
        if os.path.exists(local_path):
            return os.path.getsize(local_path)
        
        # Try Supabase
        if self.supabase_enabled:
            try:
                url = self.url(name)
                response = requests.head(url, timeout=5)
                if response.status_code == 200:
                    content_length = response.headers.get('content-length')
                    if content_length:
                        return int(content_length)
            except:
                pass
        
        return 0