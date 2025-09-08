#!/usr/bin/env python3
"""
Configure Auto Account 2 for Facebook posting
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def configure_auto_account2():
    """Configure Auto Account 2"""
    print("🚗 AUTOSELL.MX - CONFIGURING AUTO ACCOUNT 2")
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
    
    # Your app credentials (shared across all accounts)
    app_id = "2168203123683107"
    app_secret = "fa9849c56acdbd7000c89e2fe900d866"
    
    print(f"✅ App ID: {app_id}")
    print(f"✅ App Secret: {app_secret}")
    print()
    
    # Auto Account 2 configuration
    print("🤖 CONFIGURING AUTO ACCOUNT 2")
    print("-" * 40)
    print("This account will post automatically at 2:00 PM daily")
    print()
    
    print("⚠️  IMPORTANT: Get credentials from your SECOND Facebook account!")
    print("1. Go to Graph API Explorer")
    print("2. Select app: autosell-upload-post")
    print("3. Switch to your second Facebook account")
    print("4. Generate new access token")
    print("5. Copy the token and User ID")
    print()
    
    # Get credentials from user
    access_token = input("Access Token for Auto Account 2: ").strip()
    user_id = input("User ID for Auto Account 2: ").strip()
    
    if not access_token or not user_id:
        print("❌ Access Token and User ID are required!")
        return False
    
    # For personal profiles, page_id is the same as user_id
    page_id = user_id
    
    print(f"✅ Access Token: {access_token[:20]}...")
    print(f"✅ User ID: {user_id}")
    print(f"✅ Page ID: {page_id}")
    print()
    
    # Configure the account
    payload = {
        "name": "Auto Account 2",
        "account_type": "auto",
        "access_token": access_token,
        "page_id": page_id,
        "user_id": user_id,
        "app_id": app_id,
        "app_secret": app_secret,
        "automation_config": {
            "auto_posting": True,
            "schedule": {
                "time": "14:00",  # 2:00 PM
                "days": [1, 2, 3, 4, 5],  # Monday to Friday
                "max_posts_per_day": 3
            }
        }
    }
    
    try:
        print("🔄 Sending configuration to backend...")
        response = requests.post(f"{BASE_URL}/facebook/accounts", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Auto Account 2 configured successfully!")
            print(f"✅ Account ID: {result['id']}")
            print()
            print("🎯 Next steps:")
            print("1. Test posting with Auto Account 2")
            print("2. Configure Manual Account")
            print("3. Enable automatic daily posting")
            return True
        else:
            print(f"❌ Failed to configure account: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error configuring account: {e}")
        return False

if __name__ == "__main__":
    configure_auto_account2()