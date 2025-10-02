#!/usr/bin/env python3
"""
Google Drive Setup Script for Autosell.mx
Helps you set up Google Drive integration
"""

import os
import sys
import json
import requests
from pathlib import Path

def check_credentials_file():
    """Check if credentials file exists"""
    print("🔍 Checking for Google Drive credentials...")
    
    credentials_file = "drive_credentials_n8n.json"
    
    if os.path.exists(credentials_file):
        print(f"✅ Credentials file found: {credentials_file}")
        try:
            with open(credentials_file, 'r') as f:
                creds = json.load(f)
            print(f"📋 Client ID: {creds.get('client_id', 'Not found')[:20]}...")
            print(f"📋 Project ID: {creds.get('project_id', 'Not found')}")
            return True
        except Exception as e:
            print(f"❌ Invalid credentials file: {e}")
            return False
    else:
        print(f"❌ Credentials file not found: {credentials_file}")
        print("\n📋 SETUP REQUIRED:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Enable Google Drive API")
        print("3. Create OAuth2 credentials (Desktop application)")
        print("4. Download JSON file")
        print(f"5. Save as: {credentials_file}")
        print("6. Add redirect URI: http://localhost:8081/")
        return False

def test_drive_authentication():
    """Test Drive service authentication"""
    print("\n🔍 Testing Drive authentication...")
    
    try:
        sys.path.append('.')
        from app.services.drive_service import drive_service
        
        print("🔄 Attempting authentication...")
        success = drive_service.authenticate()
        
        if success:
            print("✅ Drive authentication successful!")
            return True
        else:
            print("❌ Drive authentication failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during authentication: {e}")
        return False

def test_api_connection():
    """Test Drive connection via API"""
    print("\n🔍 Testing API connection...")
    
    try:
        response = requests.post("http://localhost:8000/drive/test-connection", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ API connection successful!")
                print(f"📋 Message: {result.get('message')}")
                return True
            else:
                print(f"❌ API connection failed: {result.get('message')}")
                return False
        else:
            print(f"❌ API request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def main():
    """Run Google Drive setup"""
    print("🚀 Google Drive Setup for Autosell.mx")
    print("=" * 40)
    
    # Check credentials
    creds_ok = check_credentials_file()
    
    if not creds_ok:
        print("\n❌ SETUP INCOMPLETE")
        print("📋 Please follow the steps above to get credentials")
        return
    
    # Test authentication
    auth_ok = test_drive_authentication()
    
    # Test API connection
    api_ok = test_api_connection()
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 SETUP RESULTS")
    print("=" * 40)
    print(f"Credentials File: {'✅' if creds_ok else '❌'}")
    print(f"Drive Authentication: {'✅' if auth_ok else '❌'}")
    print(f"API Connection: {'✅' if api_ok else '❌'}")
    
    if creds_ok and auth_ok and api_ok:
        print("\n🎉 GOOGLE DRIVE SETUP COMPLETE!")
        print("✅ Your system is 100% functional")
        print("🚀 Ready for photo uploads and Drive integration")
        print("\n📋 Next steps:")
        print("1. Go to http://localhost:5173/photos")
        print("2. Select a vehicle and upload photos")
        print("3. Verify photos appear with Drive thumbnails")
    else:
        print("\n⚠️  SETUP INCOMPLETE")
        print("📋 Please check the issues above and retry")

if __name__ == "__main__":
    main()
