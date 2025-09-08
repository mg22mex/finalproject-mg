#!/usr/bin/env python3
"""
Test Multiple Facebook Accounts System
Demonstrates the functionality of the 3-account setup
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_accounts_status():
    """Test getting accounts status"""
    print("🔍 Testing Accounts Status...")
    
    try:
        response = requests.get(f"{BASE_URL}/facebook/accounts/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Found {data['total_accounts']} accounts:")
            print(f"   - Manual accounts: {data['manual_accounts']}")
            print(f"   - Auto accounts: {data['auto_accounts']}")
            print(f"   - Active accounts: {data['active_accounts']}")
            print(f"   - Configured accounts: {data['configured_accounts']}")
            
            for account in data['accounts']:
                status = "✅ Configured" if account['is_configured'] else "⚠️  Not Configured"
                print(f"   - {account['name']} ({account['account_type']}): {status}")
            
            return data
        else:
            print(f"❌ Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_manual_post(account_id, vehicle_id):
    """Test manual posting to a specific account"""
    print(f"\n📝 Testing Manual Post to Account {account_id}...")
    
    post_data = {
        "message": f"🚗 Test manual post from Account {account_id} at {datetime.now().strftime('%H:%M')}",
        "vehicle_id": vehicle_id,
        "platform": "facebook"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/facebook/accounts/{account_id}/manual-post",
            json=post_data
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Manual post created successfully!")
            print(f"   - Post ID: {data['id']}")
            print(f"   - Status: {data['status']}")
            print(f"   - Account: {data['account_id']}")
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_automation_control():
    """Test automation start/stop"""
    print(f"\n🤖 Testing Automation Control...")
    
    # Start automation
    try:
        response = requests.post(f"{BASE_URL}/facebook/start-automation")
        if response.status_code == 200:
            print("✅ Automation started successfully")
        else:
            print(f"❌ Error starting automation: {response.status_code}")
    except Exception as e:
        print(f"❌ Error starting automation: {e}")
    
    # Check status
    try:
        response = requests.get(f"{BASE_URL}/facebook/status")
        if response.status_code == 200:
            data = response.json()
            print(f"   - Automation active: {data['is_active']}")
            print(f"   - Posts this week: {data['posts_last_week']}")
            print(f"   - Active vehicles: {data['active_vehicles']}")
    except Exception as e:
        print(f"❌ Error checking status: {e}")

def main():
    """Main test function"""
    print("🧪 MULTIPLE FACEBOOK ACCOUNTS SYSTEM TEST")
    print("=" * 60)
    
    # Test 1: Check accounts status
    accounts_data = test_accounts_status()
    if not accounts_data:
        print("❌ Cannot proceed without accounts data")
        return
    
    # Test 2: Test manual posting to each account
    print(f"\n📤 Testing Manual Posting...")
    for account in accounts_data['accounts']:
        if account['account_type'] == 'manual':
            test_manual_post(account['id'], 1)  # Use vehicle ID 1 for testing
        else:
            print(f"⏭️  Skipping manual post test for {account['name']} (auto account)")
    
    # Test 3: Test automation control
    test_automation_control()
    
    # Test 4: Show current posts
    print(f"\n📊 Current Posts Status...")
    try:
        response = requests.get(f"{BASE_URL}/facebook/posts?limit=5")
        if response.status_code == 200:
            posts = response.json()
            print(f"✅ Found {len(posts)} recent posts:")
            for post in posts[:3]:  # Show first 3
                account_name = next((acc['name'] for acc in accounts_data['accounts'] 
                                   if acc['id'] == post.get('account_id')), 'Unknown')
                print(f"   - Post {post['id']}: {post['status']} via {account_name}")
        else:
            print(f"❌ Error getting posts: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting posts: {e}")
    
    print(f"\n🎯 Test Summary:")
    print(f"   - System supports {accounts_data['total_accounts']} Facebook accounts")
    print(f"   - Manual accounts: {accounts_data['manual_accounts']}")
    print(f"   - Auto accounts: {accounts_data['auto_accounts']}")
    print(f"   - Ready for credential configuration!")
    
    print(f"\n🚀 Next Steps:")
    print(f"   1. Configure Facebook credentials using configure_accounts_example.py")
    print(f"   2. Test real posting to Facebook")
    print(f"   3. Enable automatic daily reposting")
    print(f"   4. Monitor performance and engagement")

if __name__ == "__main__":
    main()
