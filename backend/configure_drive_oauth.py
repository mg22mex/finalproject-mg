#!/usr/bin/env python3
"""
Configure Google Drive OAuth2 credentials for Autosell.mx
This script helps you set up OAuth2 credentials for Google Drive API
using the same credentials you're already using for n8n.
"""

import os
import json
import sys
from pathlib import Path

def main():
    print("🔧 Google Drive OAuth2 Configuration for Autosell.mx")
    print("=" * 60)
    
    # Check if credentials file exists
    credentials_file = "drive_credentials_n8n.json"
    token_file = "drive_token.json"
    
    if os.path.exists(credentials_file):
        print(f"✅ Found existing credentials file: {credentials_file}")
    else:
        print(f"❌ Credentials file not found: {credentials_file}")
        print("\n📋 To set up Google Drive OAuth2 credentials:")
        print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
        print("2. Select your project (the same one you use for n8n)")
        print("3. Go to 'APIs & Services' > 'Credentials'")
        print("4. Click 'Create Credentials' > 'OAuth 2.0 Client IDs'")
        print("5. Choose 'Desktop application'")
        print("6. Download the JSON file and save it as 'drive_credentials.json'")
        print("7. Run this script again")
        return
    
    # Load credentials
    try:
        with open(credentials_file, 'r') as f:
            credentials = json.load(f)
        print("✅ Credentials file loaded successfully")
    except Exception as e:
        print(f"❌ Error loading credentials: {e}")
        return
    
    # Check if token file exists
    if os.path.exists(token_file):
        print(f"✅ Found existing token file: {token_file}")
        print("🎉 OAuth2 setup appears to be complete!")
        return
    
    print("\n🔐 First-time OAuth2 authentication required")
    print("This will open a browser window for Google authentication...")
    
    # Test the Drive service
    try:
        from app.services.drive_service import drive_service
        
        print("🔄 Testing Google Drive API connection...")
        if drive_service.authenticate():
            print("✅ Google Drive API authentication successful!")
            print("🎉 OAuth2 setup complete!")
            print(f"📁 Token saved to: {token_file}")
        else:
            print("❌ Google Drive API authentication failed")
            print("💡 Make sure you have the correct credentials file")
            
    except Exception as e:
        print(f"❌ Error during authentication: {e}")
        print("💡 Make sure all required packages are installed:")
        print("   pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")

if __name__ == "__main__":
    main()
