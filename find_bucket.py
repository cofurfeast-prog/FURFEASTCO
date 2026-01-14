#!/usr/bin/env python
import requests

def find_correct_bucket():
    print("=== FINDING CORRECT SUPABASE BUCKET ===")
    
    base_url = "https://wivxshghrwmgxstaowjl.supabase.co"
    
    # Test with a simple file that might exist
    test_files = [
        "hero/465755b5-c73e-462e-adf1-6049fe893789_wmremove-transformed.jpeg",  # From previous tests
        "products/06364022-3911-47a3-a980-eb46f259cad4_images.jpeg"  # From previous tests
    ]
    
    # Common bucket name patterns
    bucket_names = [
        "FurfeastCo.",
        "FurfeastCo", 
        "furfeastco",
        "furfeast-co",
        "furfeast",
        "images",
        "media",
        "uploads",
        "storage"
    ]
    
    for test_file in test_files:
        print(f"\nTesting with file: {test_file}")
        for bucket in bucket_names:
            url = f"{base_url}/storage/v1/object/public/{bucket}/{test_file}"
            try:
                response = requests.head(url, timeout=5)
                print(f"  Bucket '{bucket}': Status {response.status_code}")
                if response.status_code == 200:
                    print(f"  ✓ SUCCESS! Found working bucket: '{bucket}'")
                    return bucket
            except Exception as e:
                print(f"  Bucket '{bucket}': Error - {e}")
    
    print("\nNo working bucket found with test files. Let's try a different approach...")
    
    # Try to access the storage API directly
    storage_url = f"{base_url}/storage/v1/bucket"
    print(f"\nTrying to access storage API: {storage_url}")
    try:
        response = requests.get(storage_url, timeout=10)
        print(f"Storage API Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Storage API Error: {e}")
    
    return None

if __name__ == "__main__":
    result = find_correct_bucket()
    if result:
        print(f"\n🎉 Use this bucket name: '{result}'")
    else:
        print(f"\n❌ Could not find correct bucket name")