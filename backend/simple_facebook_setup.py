#!/usr/bin/env python3
"""
Simple Facebook Credentials Setup
Guides you through setting up your 3 Facebook accounts
"""

import requests
import json
import os

BASE_URL = "http://localhost:8000"

def print_header():
    print("🚗 AUTOSELL.MX - FACEBOOK SETUP WIZARD")
    print("=" * 50)
    print("Setting up your 3 Facebook accounts for car listing automation")
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
    print("Go to: https://developers.facebook.com/")
    print("Select your app: autosell-upload-post")
    print("Copy these values:")
    print()
    
    app_id = input("App ID: ").strip()
    app_secret = input("App Secret: ").strip()
    
    if not app_id or not app_secret:
        print("❌ App ID and App Secret are required!")
        return None, None
    
    return app_id, app_secret

def get_account_info(account_name, account_type):
    """Get individual account information"""
    print(f"\n👤 STEP {account_name}: {account_type} ACCOUNT")
    print("-" * 40)
    
    if account_type == "Manual":
        print("This account will only post when you manually trigger it")
    else:
        print(f"This account will post automatically at scheduled times")
    
    print("\nFrom Graph API Explorer, copy these values:")
    
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

def main():
    print_header()
    
    # Check backend
    if not check_backend():
        return
    
    print("🎯 Let's set up your Facebook accounts!")
    print()
    
    # Get app credentials
    app_id, app_secret = get_app_credentials()
    if not app_id or not app_secret:
        return
    
    print(f"\n✅ App credentials saved!")
    print()
    
    # Configure Manual Account
    print("🔄 Configuring Manual Account...")
    manual_data = get_account_info("2", "Manual")
    if manual_data:
        manual_config = {
            "name": "Manual Account",
            "account_type": "manual",
            **manual_data,
            "automation_config": {
                "auto_posting": False,
                "manual_only": True
            }
        }
        
        if configure_account(manual_config, app_id, app_secret):
            print("✅ Manual Account ready!")
        else:
            print("❌ Manual Account setup failed")
            return
    else:
        return
    
    # Configure Auto Account 1
    print("\n🔄 Configuring Auto Account 1...")
    auto1_data = get_account_info("3", "Auto")
    if auto1_data:
        auto1_config = {
            "name": "Auto Account 1",
            "account_type": "auto",
            **auto1_data,
            "automation_config": {
                "auto_posting": True,
                "schedule": {
                    "time": "09:00",
                    "days": [1, 2, 3, 4, 5],
                    "max_posts_per_day": 3
                }
            }
        }
        
        if configure_account(auto1_config, app_id, app_secret):
            print("✅ Auto Account 1 ready!")
        else:
            print("❌ Auto Account 1 setup failed")
            return
    else:
        return
    
    # Configure Auto Account 2
    print("\n🔄 Configuring Auto Account 2...")
    auto2_data = get_account_info("4", "Auto")
    if auto2_data:
        auto2_config = {
            "name": "Auto Account 2",
            "account_type": "auto",
            **auto2_data,
            "automation_config": {
                "auto_posting": True,
                "schedule": {
                    "time": "14:00",
                    "days": [1, 2, 3, 4, 5],
                    "max_posts_per_day": 3
                }
            }
        }
        
        if configure_account(auto2_config, app_id, app_secret):
            print("✅ Auto Account 2 ready!")
        else:
            print("❌ Auto Account 2 setup failed")
            return
    else:
        return
    
    print("\n🎉 ALL ACCOUNTS CONFIGURED SUCCESSFULLY!")
    print("=" * 50)
    print("Your Facebook posting system is ready!")
    print("\nNext steps:")
    print("1. Test posting with: python test_multiple_accounts.py")
    print("2. Check status in your web interface")
    print("3. Start automatic posting when ready")

if __name__ == "__main__":
    main()
