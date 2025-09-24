#!/usr/bin/env python3
"""
Test script for n8n workflows
Tests all webhook endpoints and workflow functionality
"""

import requests
import json
import time
from datetime import datetime

# n8n webhook URLs
N8N_BASE_URL = "http://localhost:5678"
WEBHOOKS = {
    "facebook_post": f"{N8N_BASE_URL}/webhook/facebook-post",
    "sync_sheets": f"{N8N_BASE_URL}/webhook/sync-sheets", 
    "process_vehicle": f"{N8N_BASE_URL}/webhook/process-vehicle"
}

def test_webhook_connectivity():
    """Test if n8n webhooks are accessible"""
    print("🔍 Testing n8n Webhook Connectivity...")
    print("=" * 50)
    
    for name, url in WEBHOOKS.items():
        try:
            response = requests.get(url, timeout=10)
            print(f"✅ {name}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {name}: {e}")
    
    print()

def test_facebook_workflow():
    """Test Facebook posting workflow"""
    print("🤖 Testing Facebook Workflow...")
    print("=" * 50)
    
    test_data = {
        "account_type": "auto",
        "message": f"🚗 Test post from Autosell.mx automation! - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "access_token": "test_token"  # This will fail but tests the workflow
    }
    
    try:
        response = requests.post(
            WEBHOOKS["facebook_post"],
            json=test_data,
            timeout=30
        )
        print(f"✅ Facebook workflow triggered: {response.status_code}")
        if response.text:
            print(f"   Response: {response.text[:100]}...")
    except requests.exceptions.RequestException as e:
        print(f"❌ Facebook workflow failed: {e}")
    
    print()

def test_sheets_sync_workflow():
    """Test Google Sheets sync workflow"""
    print("📊 Testing Google Sheets Sync Workflow...")
    print("=" * 50)
    
    test_data = {
        "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
        "vehicle_id": "test_123"
    }
    
    try:
        response = requests.post(
            WEBHOOKS["sync_sheets"],
            json=test_data,
            timeout=30
        )
        print(f"✅ Sheets sync workflow triggered: {response.status_code}")
        if response.text:
            print(f"   Response: {response.text[:100]}...")
    except requests.exceptions.RequestException as e:
        print(f"❌ Sheets sync workflow failed: {e}")
    
    print()

def test_vehicle_processing_workflow():
    """Test vehicle processing workflow"""
    print("🚗 Testing Vehicle Processing Workflow...")
    print("=" * 50)
    
    test_data = {
        "vehicle_id": "test_vehicle_123"
    }
    
    try:
        response = requests.post(
            WEBHOOKS["process_vehicle"],
            json=test_data,
            timeout=30
        )
        print(f"✅ Vehicle processing workflow triggered: {response.status_code}")
        if response.text:
            print(f"   Response: {response.text[:100]}...")
    except requests.exceptions.RequestException as e:
        print(f"❌ Vehicle processing workflow failed: {e}")
    
    print()

def main():
    """Main test function"""
    print("🚀 Autosell.mx - n8n Workflow Testing")
    print("=" * 60)
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test webhook connectivity
    test_webhook_connectivity()
    
    # Test individual workflows
    test_facebook_workflow()
    test_sheets_sync_workflow()
    test_vehicle_processing_workflow()
    
    print("🎉 n8n Workflow Testing Complete!")
    print("=" * 60)
    print("📋 Next Steps:")
    print("1. Access n8n dashboard: http://localhost:5678")
    print("2. Import workflow JSON files from n8n_workflows/ folder")
    print("3. Configure OAuth2 credentials for Google services")
    print("4. Test workflows with real data")
    print("5. Monitor execution logs in n8n dashboard")

if __name__ == "__main__":
    main()