#!/usr/bin/env python3
"""
Use the same OAuth2 client that n8n is using for Google Drive API
"""

import json
import os

def create_n8n_compatible_credentials():
    """Create credentials file using the same OAuth2 client as n8n"""
    
    # The OAuth2 client ID from your Google Cloud Console
    client_id = "108732765716-p5vd8shfs9ied3nujmmaigcf4mes2hm3.apps.googleusercontent.com"
    
    # You need to get the client secret from Google Cloud Console
    print("🔑 Creating n8n-compatible credentials...")
    print(f"📋 Client ID: {client_id}")
    print("⚠️  You need to get the client secret from Google Cloud Console")
    
    # Create credentials file
    credentials = {
        "installed": {
            "client_id": client_id,
            "client_secret": "YOUR_CLIENT_SECRET_HERE",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "redirect_uris": [
                "http://localhost:5678/rest/oauth2-credential/callback",
                "http://localhost:8080/"
            ]
        }
    }
    
    with open('drive_credentials_n8n.json', 'w') as f:
        json.dump(credentials, f, indent=2)
    
    print("✅ Created drive_credentials_n8n.json")
    print("\n📋 Next steps:")
    print("1. Go to Google Cloud Console")
    print("2. Find your OAuth2 client: 108732765716-p5vd8shfs9ied3nujmmaigcf4mes2hm3")
    print("3. Copy the client secret")
    print("4. Update the 'YOUR_CLIENT_SECRET_HERE' in drive_credentials_n8n.json")
    print("5. Run: python configure_drive_oauth.py")
    
    return True

if __name__ == "__main__":
    create_n8n_compatible_credentials()
