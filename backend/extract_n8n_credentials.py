#!/usr/bin/env python3
"""
Extract Google OAuth2 credentials from n8n database and use them for Drive API
"""

import sqlite3
import json
import os
import base64
from cryptography.fernet import Fernet
import hashlib

def extract_n8n_credentials():
    """Extract Google OAuth2 credentials from n8n database"""
    
    # n8n database path
    n8n_db_path = os.path.expanduser("~/.n8n/database.sqlite")
    
    if not os.path.exists(n8n_db_path):
        print("❌ n8n database not found at ~/.n8n/database.sqlite")
        return None
    
    try:
        # Connect to n8n database
        conn = sqlite3.connect(n8n_db_path)
        cursor = conn.cursor()
        
        # Get Google credentials
        cursor.execute("""
            SELECT name, data, type 
            FROM credentials_entity 
            WHERE type LIKE '%google%' OR name LIKE '%google%'
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            print("❌ No Google credentials found in n8n database")
            return None
        
        print(f"✅ Found {len(results)} Google credential(s) in n8n")
        
        # Try to decrypt the credentials
        for name, encrypted_data, cred_type in results:
            print(f"📋 Credential: {name} (Type: {cred_type})")
            
            try:
                # n8n uses a simple encryption - let's try to decode it
                # The data appears to be base64 encoded
                decoded_data = base64.b64decode(encrypted_data)
                print(f"🔓 Decoded data length: {len(decoded_data)} bytes")
                
                # Try to parse as JSON
                try:
                    # The data might be encrypted with a key derived from n8n's secret
                    # Let's try to extract the OAuth2 token directly
                    credential_data = json.loads(decoded_data.decode('utf-8'))
                    print("✅ Successfully decoded credential data")
                    return credential_data
                except:
                    print("⚠️  Could not parse as JSON, trying alternative methods...")
                    
                    # Try to extract OAuth2 tokens from the raw data
                    data_str = decoded_data.decode('utf-8', errors='ignore')
                    if 'access_token' in data_str or 'refresh_token' in data_str:
                        print("✅ Found OAuth2 tokens in data")
                        return data_str
                        
            except Exception as e:
                print(f"⚠️  Could not decode credential {name}: {e}")
                continue
        
        print("❌ Could not extract usable credentials from n8n")
        return None
        
    except Exception as e:
        print(f"❌ Error accessing n8n database: {e}")
        return None

def create_drive_credentials_from_n8n():
    """Create Drive credentials file from n8n data"""
    
    print("🔍 Extracting credentials from n8n...")
    n8n_data = extract_n8n_credentials()
    
    if not n8n_data:
        print("❌ Could not extract credentials from n8n")
        return False
    
    print("✅ Credentials extracted successfully")
    print("📝 Note: You may need to re-authenticate for Drive API access")
    
    # Create a simple credentials file that points to the n8n tokens
    credentials_info = {
        "client_id": "108732765716-p5vd8shfs9ied3nujmmaigcf4mes2hm3.apps.googleusercontent.com",
        "client_secret": "YOUR_CLIENT_SECRET_HERE",  # You'll need to get this from Google Cloud Console
        "redirect_uri": "http://localhost:5678/rest/oauth2-credential/callback",
        "note": "Using n8n OAuth2 credentials - you may need to re-authenticate for Drive API"
    }
    
    with open('drive_credentials_from_n8n.json', 'w') as f:
        json.dump(credentials_info, f, indent=2)
    
    print("✅ Created drive_credentials_from_n8n.json")
    print("📋 Next steps:")
    print("1. Get your client secret from Google Cloud Console")
    print("2. Update the client_secret in the file")
    print("3. Run the Drive authentication")
    
    return True

if __name__ == "__main__":
    create_drive_credentials_from_n8n()
