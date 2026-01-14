#!/usr/bin/env python
import requests

def test_profile_picture_url():
    print("=== TESTING SPECIFIC PROFILE PICTURE URL ===")
    
    # The exact URL from the database
    profile_url = "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/public/FurfeastCo./profiles/e8b8d30a-4146-4c47-b346-3e5e229ab8ad_cutie.jpg"
    
    print(f"Testing URL: {profile_url}")
    
    try:
        response = requests.head(profile_url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'Unknown')}")
        
        if response.status_code == 200:
            print("SUCCESS! The profile picture URL is accessible.")
            print("The issue might be in the browser or template rendering.")
        elif response.status_code == 404:
            print("NOT FOUND! The profile picture file doesn't exist in Supabase.")
        elif response.status_code == 400:
            print("BAD REQUEST! There might be an issue with the URL format or bucket.")
        else:
            print(f"OTHER ERROR: {response.status_code}")
            
        # Try to get the actual response content for more info
        if response.status_code != 200:
            try:
                full_response = requests.get(profile_url, timeout=10)
                print(f"Response body: {full_response.text[:200]}...")
            except:
                pass
                
    except Exception as e:
        print(f"Error accessing URL: {e}")

if __name__ == "__main__":
    test_profile_picture_url()