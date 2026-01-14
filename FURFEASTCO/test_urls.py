import requests

# Test URLs from the output
test_urls = [
    "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/public/FurfeastCo./hero/465755b5-c73e-462e-adf1-6049fe893789_wmremove-transformed.jpeg",
    "https://wivxshghrwmgxstaowjl.supabase.co/storage/v1/object/public/FurfeastCo./products/06364022-3911-47a3-a980-eb46f259cad4_images.jpeg"
]

print("Testing Supabase URLs...")
for url in test_urls:
    try:
        response = requests.head(url, timeout=10)
        print(f"URL: {url}")
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type', 'Unknown')}")
        print("---")
    except Exception as e:
        print(f"Error testing {url}: {e}")
        print("---")