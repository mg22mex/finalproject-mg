#!/usr/bin/env python3
"""
Interactive Facebook Credentials Setup
Guides you through setting up your 3 Facebook accounts
"""

import requests
import json
import os
from getpass import getpass

BASE_URL = "http://localhost:8000"

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print("❌ Backend is not responding properly")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("💡 Make sure to run: python main_fixed.py")
        return False

def get_facebook_credentials():
    """Get Facebook credentials from user"""
    print("\n🔐 FACEBOOK CREDENTIALS SETUP")
    print("=" * 50)
    
    # App credentials (shared across all accounts)
    print("\n📱 FACEBOOK APP CREDENTIALS (Shared)")
    print("Get these from: https://developers.facebook.com/")
    app_id = input("App ID: ").strip()
    app_secret = getpass("App Secret: ").strip()
    
    if not app_id or not app_secret:
        print("❌ App ID and App Secret are required!")
        return None
    
    # Account 1: Manual Account
    print("\n👤 ACCOUNT 1: Manual Account")
    print("This account will only post when you manually trigger it")
    manual_token = getpass("Access Token: ").strip()
    manual_page_id = input("Page ID: ").strip()
    manual_user_id = input("User ID: ").strip()
    
    # Account 2: Auto Account 1
    print("\n🤖 ACCOUNT 2: Auto Account 1")
    print("This account will post automatically at 9:00 AM")
    auto1_token = getpass("Access Token: ").strip()
    auto1_page_id = input("Page ID: ").strip()
    auto1_user_id = input("User ID: ").strip()
    
    # Account 3: Auto Account 2
    print("\n🤖 ACCOUNT 3: Auto Account 2")
    print("This account will post automatically at 2:00 PM")
    auto2_token = getpass("Access Token: ").strip()
    auto2_page_id = input("Page ID: ").strip()
    auto2_user_id = input("User ID: ").strip()
    
    return {
        "app_id": app_id,
        "app_secret": app_secret,
        "accounts": {
            "manual": {
                "name": "Manual Account",
                "account_type": "manual",
                "access_token": manual_token,
                "page_id": manual_page_id,
                "user_id": manual_user_id,
                "app_id": app_id,
                "app_secret": app_secret,
                "automation_config": {
                    "auto_posting": False,
                    "manual_only": True
                }
            },
            "auto1": {
                "name": "Auto Account 1",
                "account_type": "auto",
                "access_token": auto1_token,
                "page_id": auto1_page_id,
                "user_id": auto1_user_id,
                "app_id": app_id,
                "app_secret": app_secret,
                "automation_config": {
                    "auto_posting": True,
                    "schedule": {
                        "time": "09:00",
                        "days": [1, 2, 3, 4, 5],
                        "max_posts_per_day": 3
                    }
                }
            },
            "auto2": {
                "name": "Auto Account 2",
                "account_type": "auto",
                "access_token": auto2_token,
                "page_id": auto2_page_id,
                "user_id": auto2_user_id,
                "app_id": app_id,
                "app_secret": app_secret,
                "automation_config": {
                    "auto_posting": True,
                    "schedule": {
                        "time": "14:00",
                        "days": [1, 2, 3, 4, 5],
                        "max_posts_per_day": 3
                    }
                }
            }
        }
    }

def configure_account(account_id, config):
    """Configure a Facebook account"""
    print(f"\n🔧 Configuring {config['name']}...")
    
    try:
        response = requests.put(f"{BASE_URL}/facebook/accounts/{account_id}", json=config)
        if response.status_code == 200:
            print(f"✅ {config['name']} configured successfully!")
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_account(account_id, config):
    """Test if account is working"""
    print(f"\n🧪 Testing {config['name']}...")
    
    try:
        # Test manual post
        post_data = {
            "message": f"🧪 Test post from {config['name']} - System configuration test",
            "vehicle_id": 1,
            "platform": "facebook"
        }
        
        response = requests.post(
            f"{BASE_URL}/facebook/accounts/{account_id}/manual-post",
            json=post_data
        )
        
        if response.status_code == 200:
            print(f"✅ {config['name']} is working! Test post created.")
            return True
        else:
            print(f"❌ Test failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 FACEBOOK MULTI-ACCOUNT SETUP WIZARD")
    print("=" * 60)
    
    # Check backend
    if not check_backend():
        return
    
    # Get credentials
    credentials = get_facebook_credentials()
    if not credentials:
        return
    
    # Show summary
    print("\n📋 CONFIGURATION SUMMARY")
    print("=" * 40)
    print(f"App ID: {credentials['app_id']}")
    print(f"App Secret: {'*' * len(credentials['app_secret'])}")
    print(f"Manual Account: {credentials['accounts']['manual']['name']}")
    print(f"Auto Account 1: {credentials['accounts']['auto1']['name']}")
    print(f"Auto Account 2: {credentials['accounts']['auto2']['name']}")
    
    # Confirm
    confirm = input("\n🤔 Proceed with this configuration? (y/N): ")
    if confirm.lower() != 'y':
        print("👋 Setup cancelled.")
        return
    
    # Configure accounts
    print("\n🔧 CONFIGURING ACCOUNTS...")
    success_count = 0
    
    # Account 1 (Manual)
    if configure_account(1, credentials['accounts']['manual']):
        success_count += 1
    
    # Account 2 (Auto 1)
    if configure_account(2, credentials['accounts']['auto1']):
        success_count += 1
    
    # Account 3 (Auto 2)
    if configure_account(3, credentials['accounts']['auto2']):
        success_count += 1
    
    print(f"\n📊 Configuration Results: {success_count}/3 accounts configured")
    
    if success_count == 3:
        print("\n🎉 ALL ACCOUNTS CONFIGURED SUCCESSFULLY!")
        
        # Test accounts
        print("\n🧪 TESTING ACCOUNTS...")
        test_success = 0
        
        if test_account(1, credentials['accounts']['manual']):
            test_success += 1
        if test_account(2, credentials['accounts']['auto1']):
            test_success += 1
        if test_account(3, credentials['accounts']['auto2']):
            test_success += 1
        
        print(f"\n🧪 Test Results: {test_success}/3 accounts working")
        
        if test_success == 3:
            print("\n🚀 SYSTEM READY FOR PRODUCTION!")
            print("\n🎯 What you can do now:")
            print("   1. Manual posting via Account 1")
            print("   2. Automatic daily posting via Accounts 2 & 3")
            print("   3. Monitor all accounts from the dashboard")
            print("   4. Schedule different posting times")
        else:
            print("\n⚠️  Some accounts have issues. Check the error messages above.")
    else:
        print("\n❌ Some accounts failed to configure.")
        print("Check the error messages and try again.")

if __name__ == "__main__":
    main()
