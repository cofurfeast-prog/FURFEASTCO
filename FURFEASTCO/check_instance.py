#!/usr/bin/env python3
"""
Check Google Cloud SQL instance status and proceed with migration
"""
import subprocess
import time

def check_instance_status():
    """Check if the SQL instance is ready"""
    result = subprocess.run(
        ["gcloud", "sql", "instances", "describe", "furfeast-db", "--format=value(state)"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def main():
    print("Checking Google Cloud SQL instance status...")
    
    while True:
        status = check_instance_status()
        print(f"Current status: {status}")
        
        if status == "RUNNABLE":
            print("✅ Instance is ready!")
            print("\nNext steps:")
            print("1. Run: gcloud sql databases create furfeast --instance=furfeast-db")
            print("2. Run: gcloud sql users create furfeast-user --instance=furfeast-db --password=FurfeastDB2024!")
            print("3. Run: python complete_migration.py")
            break
        elif status == "PENDING_CREATE":
            print("⏳ Instance is still being created... waiting 30 seconds")
            time.sleep(30)
        else:
            print(f"❌ Unexpected status: {status}")
            break

if __name__ == "__main__":
    main()