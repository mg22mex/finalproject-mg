#!/usr/bin/env python3
"""
Test script for Google Drive OAuth authentication
"""

import os
import sys
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google Drive API scopes
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]

def test_oauth():
    """Test OAuth authentication"""
    try:
        print("🔄 Testing Google Drive OAuth authentication...")
        
        creds = None
        token_file = 'drive_token.json'
        credentials_file = 'drive_credentials_n8n.json'
        
        print(f"📁 Token file: {token_file}")
        print(f"📁 Credentials file: {credentials_file}")
        
        # Load existing credentials
        if os.path.exists(token_file):
            print("✅ Loading existing credentials...")
            creds = Credentials.from_authorized_user_file(token_file, SCOPES)
            print(f"📊 Credentials valid: {creds.valid if creds else False}")
        else:
            print("❌ No existing credentials found")
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            print("🔄 Starting OAuth flow...")
            if creds and creds.expired and creds.refresh_token:
                print("🔄 Refreshing expired credentials...")
                creds.refresh(Request())
            else:
                if not os.path.exists(credentials_file):
                    print(f"❌ Credentials file not found: {credentials_file}")
                    return False
                
                print("🔄 Starting OAuth flow with redirect URI: http://localhost:8081/")
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                flow.redirect_uri = 'http://localhost:8081/'
                creds = flow.run_local_server(port=8081, redirect_uri_trailing_slash=False)
                print("✅ OAuth flow completed successfully")
            
            # Save credentials
            print("💾 Saving credentials...")
            with open(token_file, 'w') as token:
                token.write(creds.to_json())
            print("✅ Credentials saved")
        
        # Build service
        print("🔧 Building Drive service...")
        service = build('drive', 'v3', credentials=creds)
        
        # Test service
        print("🧪 Testing Drive service...")
        results = service.files().list(pageSize=1).execute()
        files = results.get('files', [])
        print(f"✅ Drive service working! Found {len(files)} files")
        
        return True
        
    except Exception as e:
        print(f"❌ OAuth test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_oauth()
    if success:
        print("🎉 OAuth authentication successful!")
    else:
        print("❌ OAuth authentication failed!")
        sys.exit(1)
