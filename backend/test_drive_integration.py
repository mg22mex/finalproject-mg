#!/usr/bin/env python3
"""
Test Google Drive Integration for Autosell.mx
This script tests the Drive API integration once OAuth2 is configured.
"""

import os
import sys
import json
from pathlib import Path

def test_drive_credentials():
    """Test if Drive credentials are properly configured"""
    print("🔍 Testing Google Drive Integration")
    print("=" * 40)
    
    # Check if credentials file exists
    credentials_file = "drive_credentials_n8n.json"
    token_file = "drive_token.json"
    
    if not os.path.exists(credentials_file):
        print(f"❌ Credentials file not found: {credentials_file}")
        print("💡 Please run: ./setup_drive_credentials.sh")
        return False
    
    print(f"✅ Found credentials file: {credentials_file}")
    
    # Check if token file exists
    if not os.path.exists(token_file):
        print(f"⚠️  Token file not found: {token_file}")
        print("💡 This means first-time authentication is required")
        return False
    
    print(f"✅ Found token file: {token_file}")
    
    # Test the Drive service
    try:
        from app.services.drive_service import drive_service
        
        print("🔄 Testing Google Drive API connection...")
        if drive_service.authenticate():
            print("✅ Google Drive API authentication successful!")
            return True
        else:
            print("❌ Google Drive API authentication failed")
            return False
            
    except Exception as e:
        print(f"❌ Error during authentication: {e}")
        return False

def test_drive_endpoints():
    """Test Drive API endpoints"""
    print("\n🌐 Testing Drive API Endpoints")
    print("=" * 40)
    
    import requests
    
    base_url = "http://localhost:8000"
    
    # Test connection endpoint
    try:
        response = requests.post(f"{base_url}/drive/test-connection")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Drive test connection successful")
            else:
                print(f"⚠️  Drive test connection failed: {data.get('message')}")
        else:
            print(f"❌ Drive test connection failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing connection endpoint: {e}")

def main():
    print("🚗 Autosell.mx - Google Drive Integration Test")
    print("=" * 50)
    
    # Test credentials
    if not test_drive_credentials():
        print("\n💡 To fix this:")
        print("1. Run: ./setup_drive_credentials.sh")
        print("2. Complete OAuth2 authentication")
        print("3. Run this test again")
        return
    
    # Test endpoints
    test_drive_endpoints()
    
    print("\n🎉 Google Drive integration test complete!")
    print("🚀 You can now use the Drive features in your application")

if __name__ == "__main__":
    main()
