#!/usr/bin/env python
import requests

def test_supabase_urls():
    print("=== TESTING SUPABASE URL FORMATS ===")
    
    base_url = "https://wivxshghrwmgxstaowjl.supabase.co"
    file_path = "profiles/e8b8d30a-4146-4c47-b346-3e5e229ab8ad_cutie.jpg"
    
    # Test different bucket names
    bucket_names = [
        "FurfeastCo.",
        "FurfeastCo",
        "furfeastco",
        "furfeast-co",
        "furfeast"
    ]
    
    for bucket in bucket_names:
        url = f"{base_url}/storage/v1/object/public/{bucket}/{file_path}"
        print(f"\nTesting bucket: '{bucket}'")
        print(f"URL: {url}")
        
        try:
            response = requests.head(url, timeout=5)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("SUCCESS! This bucket name works.")
                return bucket
            elif response.status_code == 400:
                print("Bad Request - likely wrong bucket name")
            elif response.status_code == 404:
                print("Not Found - file doesn't exist in this bucket")
            else:
                print(f"Other error: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\nNone of the bucket names worked. The file might not exist in Supabase storage.")
    return None

if __name__ == "__main__":
    test_supabase_urls()