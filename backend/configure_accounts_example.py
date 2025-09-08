#!/usr/bin/env python3
"""
Facebook Accounts Configuration Script
Use this to configure your 3 Facebook accounts with real credentials
"""

import requests
import json

# Configuration for your 3 Facebook accounts
ACCOUNTS_CONFIG = {
    "Manual Account": {
        "name": "Manual Account",
        "account_type": "manual",
        "access_token": "YOUR_MANUAL_ACCOUNT_ACCESS_TOKEN",
        "page_id": "YOUR_MANUAL_ACCOUNT_PAGE_ID",
        "user_id": "YOUR_MANUAL_ACCOUNT_USER_ID",
        "app_id": "YOUR_APP_ID",
        "app_secret": "YOUR_APP_SECRET",
        "automation_config": {
            "auto_posting": False,
            "manual_only": True
        }
    },
    "Auto Account 1": {
        "name": "Auto Account 1",
        "account_type": "auto",
        "access_token": "YOUR_AUTO_ACCOUNT_1_ACCESS_TOKEN",
        "page_id": "YOUR_AUTO_ACCOUNT_1_PAGE_ID",
        "user_id": "YOUR_AUTO_ACCOUNT_1_USER_ID",
        "app_id": "YOUR_APP_ID",
        "app_secret": "YOUR_APP_SECRET",
        "automation_config": {
            "auto_posting": True,
            "schedule": {
                "time": "09:00",
                "days": [1, 2, 3, 4, 5],  # Monday to Friday
                "max_posts_per_day": 3
            }
        }
    },
    "Auto Account 2": {
        "name": "Auto Account 2",
        "account_type": "auto",
        "access_token": "YOUR_AUTO_ACCOUNT_2_ACCESS_TOKEN",
        "page_id": "YOUR_AUTO_ACCOUNT_2_PAGE_ID",
        "user_id": "YOUR_AUTO_ACCOUNT_2_USER_ID",
        "app_id": "YOUR_APP_ID",
        "app_secret": "YOUR_APP_SECRET",
        "automation_config": {
            "auto_posting": True,
            "schedule": {
                "time": "14:00",
                "days": [1, 2, 3, 4, 5],  # Monday to Friday
                "max_posts_per_day": 3
            }
        }
    }
}

def configure_account(account_id, config):
    """Configure a Facebook account"""
    url = f"http://localhost:8000/facebook/accounts/{account_id}"
    
    try:
        response = requests.put(url, json=config)
        if response.status_code == 200:
            print(f"✅ {config['name']} configured successfully!")
            return True
        else:
            print(f"❌ Error configuring {config['name']}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error configuring {config['name']}: {e}")
        return False

def main():
    """Main configuration function"""
    print("🚀 Facebook Accounts Configuration")
    print("=" * 50)
    
    print("\n📋 Before running this script:")
    print("1. Replace 'YOUR_*' values with real Facebook credentials")
    print("2. Make sure your backend is running on localhost:8000")
    print("3. Have your Facebook App ID and App Secret ready")
    print("4. Generate access tokens for each account")
    
    print("\n🔐 Required for each account:")
    print("- Access Token (User or Page token)")
    print("- Page ID (where posts will appear)")
    print("- User ID (for Marketplace listings)")
    print("- App ID and App Secret (shared)")
    
    print("\n⚠️  IMPORTANT: Keep your credentials secure!")
    print("Never commit real credentials to version control.")
    
    # Ask user if they want to proceed
    response = input("\n🤔 Do you want to configure the accounts now? (y/N): ")
    if response.lower() != 'y':
        print("👋 Configuration cancelled. Update the script with your credentials first.")
        return
    
    print("\n🔧 Configuring accounts...")
    
    success_count = 0
    for account_id, config in enumerate(ACCOUNTS_CONFIG.values(), 1):
        if configure_account(account_id, config):
            success_count += 1
    
    print(f"\n📊 Configuration Results:")
    print(f"✅ Successfully configured: {success_count}/{len(ACCOUNTS_CONFIG)} accounts")
    
    if success_count == len(ACCOUNTS_CONFIG):
        print("\n🎉 All accounts configured successfully!")
        print("🚀 You can now:")
        print("   - Use manual posting for Account 1")
        print("   - Enable automatic daily posting for Accounts 2 & 3")
        print("   - Monitor all accounts from the dashboard")
    else:
        print("\n⚠️  Some accounts failed to configure.")
        print("Check the error messages above and try again.")

if __name__ == "__main__":
    main()
