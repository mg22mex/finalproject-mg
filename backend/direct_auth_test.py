#!/usr/bin/env python3
"""
Direct Google Drive OAuth2 authentication test
"""

import os
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google Drive API scopes
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]

def test_direct_auth():
    """Test direct OAuth2 authentication"""
    print("🔐 Testing Direct Google Drive OAuth2 Authentication")
    print("=" * 60)
    
    credentials_file = 'drive_credentials_n8n.json'
    token_file = 'drive_token.json'
    
    if not os.path.exists(credentials_file):
        print(f"❌ Credentials file not found: {credentials_file}")
        return False
    
    print(f"✅ Found credentials file: {credentials_file}")
    
    try:
        creds = None
        
        # Load existing token
        if os.path.exists(token_file):
            print(f"✅ Found existing token file: {token_file}")
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Refreshing expired credentials...")
                creds.refresh(Request())
            else:
                print("🔐 Starting OAuth2 authentication...")
                print("📱 This will open a browser window for authentication...")
                
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                creds = flow.run_local_server(port=9090)  # Use fixed port 9090
            
            # Save credentials for next run
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
            print(f"✅ Token saved to: {token_file}")
        
        # Test Drive API connection
        print("🔄 Testing Google Drive API connection...")
        service = build('drive', 'v3', credentials=creds)
        
        # Test API call
        results = service.files().list(pageSize=10).execute()
        items = results.get('files', [])
        
        print(f"✅ Google Drive API connection successful!")
        print(f"📁 Found {len(items)} files in your Drive")
        
        if items:
            print("📋 Sample files:")
            for item in items[:3]:
                print(f"   - {item.get('name', 'Unknown')} (ID: {item.get('id', 'Unknown')})")
        
        return True
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False

if __name__ == "__main__":
    success = test_direct_auth()
    if success:
        print("\n🎉 Google Drive OAuth2 authentication successful!")
        print("✅ You can now use the Drive API integration")
    else:
        print("\n❌ Authentication failed")
        print("💡 Check your credentials and try again")
