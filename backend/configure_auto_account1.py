#!/usr/bin/env python3
"""
Configure Auto Account 1 for Facebook posting
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def configure_auto_account1():
    """Configure Auto Account 1"""
    print("🚗 AUTOSELL.MX - CONFIGURING AUTO ACCOUNT 1")
    print("=" * 50)
    
    # Check backend
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Backend is running and ready!")
        else:
            print("❌ Backend is not responding properly")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("💡 Make sure to run: python main_fixed.py")
        return False
    
    # Your app credentials (already known)
    app_id = "2168203123683107"
    app_secret = "fa9849c56acdbd7000c89e2fe900d866"
    
    print(f"✅ App ID: {app_id}")
    print(f"✅ App Secret: {app_secret}")
    print()
    
    # Auto Account 1 configuration
    print("🤖 CONFIGURING AUTO ACCOUNT 1")
    print("-" * 40)
    print("This account will post automatically at 9:00 AM daily")
    print()
    
    # You need to EDIT these values in the script:
    print("⚠️  IMPORTANT: Edit this script to add your values!")
    print("Replace the placeholders below with your actual values:")
    print()
    
    # EDIT THESE VALUES:
    access_token = "EAAezZBCD87yMBPazAqaNO5AoS7VXWqzObJUCRsj7Oihl9rFpZA1klyFqvp0FqICyaQQmTyKGqc0cZCLpdUPY7ufoHHskcwiRU4Wq62DOSPcxzQbIaf4ZBl5M3SZC22Pqk7XVrQUhRwHCaZAu1CNZB0hr6rlQ4wh7ZBbNNn6j0O2vemNmf2KDQqxEN33EZAmYkikBGbgA2Bw17B5Mh4YJG2fGXOZAS8eahoCHZAEBsGBzOl5BMi8uAm4ldpLGBAYhRlqbwZDZD"  # ← EDIT THIS
    user_id = "122151506120618429"  # ← This is already correct
    
    # Check if access token is properly set
    if not access_token or access_token.startswith("PASTE_YOUR"):
        print("❌ Please edit the script and add your Access Token!")
        print("1. Open this file in your editor")
        print("2. Replace the placeholder with your actual token")
        print("3. Save and run again")
        return False
    
    # For personal profiles, page_id is the same as user_id
    page_id = user_id
    
    print(f"✅ Access Token: {access_token[:20]}...")
    print(f"✅ User ID: {user_id}")
    print(f"✅ Page ID: {page_id}")
    print()
    
    # Configure the account
    payload = {
        "name": "Auto Account 1",
        "account_type": "auto",
        "access_token": access_token,
        "page_id": page_id,
        "user_id": user_id,
        "app_id": app_id,
        "app_secret": app_secret,
        "automation_config": {
            "auto_posting": True,
            "schedule": {
                "time": "09:00",
                "days": [1, 2, 3, 4, 5],  # Monday to Friday
                "max_posts_per_day": 3
            }
        }
    }
    
    try:
        print("🔄 Sending configuration to backend...")
        response = requests.post(f"{BASE_URL}/facebook/accounts", json=payload)
        
        if response.status_code == 200:
            print("✅ Auto Account 1 configured successfully!")
            print()
            print("🎯 Next steps:")
            print("1. Configure Auto Account 2")
            print("2. Configure Manual Account")
            print("3. Test posting with: python test_multiple_accounts.py")
            return True
        else:
            print(f"❌ Failed to configure account: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error configuring account: {e}")
        return False

if __name__ == "__main__":
    configure_auto_account1()
