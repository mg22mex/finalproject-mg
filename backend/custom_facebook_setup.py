#!/usr/bin/env python3
"""
Custom Facebook Credentials Setup
Choose which account to configure first
"""

import requests
import json
import os

BASE_URL = "http://localhost:8000"

def print_header():
    print("🚗 AUTOSELL.MX - CUSTOM FACEBOOK SETUP")
    print("=" * 50)
    print("Choose which account to configure first")
    print()

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Backend is running and ready!")
            return True
        else:
            print("❌ Backend is not responding properly")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("💡 Make sure to run: python main_fixed.py")
        return False

def get_app_credentials():
    """Get Facebook app credentials"""
    print("📱 STEP 1: FACEBOOK APP CREDENTIALS")
    print("-" * 40)
    print("Your app: autosell-upload-post")
    print("Status: Development mode (perfect for testing!)")
    print()
    
    # Use the values you already have
    app_id = "2168203123683107"
    app_secret = "fa9849c56acdbd7000c89e2fe900d866"
    
    print(f"✅ App ID: {app_id}")
    print(f"✅ App Secret: {app_secret}")
    print()
    
    return app_id, app_secret

def choose_account():
    """Let user choose which account to configure"""
    print("🎯 STEP 2: CHOOSE ACCOUNT TO CONFIGURE")
    print("-" * 40)
    print("Which account would you like to configure first?")
    print("1. Auto Account 1 (9:00 AM posting)")
    print("2. Auto Account 2 (2:00 PM posting)")
    print("3. Manual Account (manual posting only)")
    print("4. Configure all accounts")
    print()
    
    while True:
        choice = input("Enter your choice (1-4): ").strip()
        if choice in ['1', '2', '3', '4']:
            return choice
        print("❌ Please enter 1, 2, 3, or 4")

def get_account_info(account_name, account_type):
    """Get individual account information"""
    print(f"\n👤 CONFIGURING: {account_name}")
    print("-" * 40)
    
    if account_type == "Manual":
        print("This account will only post when you manually trigger it")
    else:
        print(f"This account will post automatically at scheduled times")
    
    print("\nFrom Graph API Explorer, copy these values:")
    print("💡 Tip: You can copy-paste the values!")
    
    access_token = input("Access Token: ").strip()
    user_id = input("User ID: ").strip()
    
    # For personal profiles, page_id is the same as user_id
    page_id = user_id
    
    if not access_token or not user_id:
        print(f"❌ Access Token and User ID are required for {account_name}!")
        return None
    
    return {
        "access_token": access_token,
        "page_id": page_id,
        "user_id": user_id
    }

def configure_account(account_data, app_id, app_secret):
    """Configure an account via the API"""
    try:
        payload = {
            "name": account_data["name"],
            "account_type": account_data["account_type"],
            "access_token": account_data["access_token"],
            "page_id": account_data["page_id"],
            "user_id": account_data["user_id"],
            "app_id": app_id,
            "app_secret": app_secret,
            "automation_config": account_data.get("automation_config", {})
        }
        
        response = requests.post(f"{BASE_URL}/facebook/accounts", json=payload)
        
        if response.status_code == 200:
            print(f"✅ {account_data['name']} configured successfully!")
            return True
        else:
            print(f"❌ Failed to configure {account_data['name']}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error configuring {account_data['name']}: {e}")
        return False

def configure_single_account(choice, app_id, app_secret):
    """Configure a single account based on choice"""
    if choice == "1":
        # Auto Account 1
        print("\n🔄 Configuring Auto Account 1...")
        data = get_account_info("Auto Account 1", "Auto")
        if data:
            config = {
                "name": "Auto Account 1",
                "account_type": "auto",
                **data,
                "automation_config": {
                    "auto_posting": True,
                    "schedule": {
                        "time": "09:00",
                        "days": [1, 2, 3, 4, 5],
                        "max_posts_per_day": 3
                    }
                }
            }
            return configure_account(config, app_id, app_secret)
    
    elif choice == "2":
        # Auto Account 2
        print("\n🔄 Configuring Auto Account 2...")
        data = get_account_info("Auto Account 2", "Auto")
        if data:
            config = {
                "name": "Auto Account 2",
                "account_type": "auto",
                **data,
                "automation_config": {
                    "auto_posting": True,
                    "schedule": {
                        "time": "14:00",
                        "days": [1, 2, 3, 4, 5],
                        "max_posts_per_day": 3
                    }
                }
            }
            return configure_account(config, app_id, app_secret)
    
    elif choice == "3":
        # Manual Account
        print("\n🔄 Configuring Manual Account...")
        data = get_account_info("Manual Account", "Manual")
        if data:
            config = {
                "name": "Manual Account",
                "account_type": "manual",
                **data,
                "automation_config": {
                    "auto_posting": False,
                    "manual_only": True
                }
            }
            return configure_account(config, app_id, app_secret)
    
    return False

def main():
    print_header()
    
    # Check backend
    if not check_backend():
        return
    
    # Get app credentials (already known)
    app_id, app_secret = get_app_credentials()
    
    print("🎯 Let's set up your Facebook accounts!")
    print("💡 Remember: Test data takes 24 hours to appear")
    print()
    
    # Choose account to configure
    choice = choose_account()
    
    if choice == "4":
        # Configure all accounts
        print("\n🔄 Configuring all accounts...")
        # This would be a loop through all accounts
        print("Feature coming soon - let's do one at a time for now")
        return
    else:
        # Configure single account
        success = configure_single_account(choice, app_id, app_secret)
        if success:
            print(f"\n✅ Account configured successfully!")
            print("\nNext steps:")
            print("1. Configure more accounts if needed")
            print("2. Test posting with: python test_multiple_accounts.py")
            print("3. Check status in your web interface")
        else:
            print(f"\n❌ Account configuration failed")

if __name__ == "__main__":
    main()
