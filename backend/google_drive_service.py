"""
Google Drive Service for Autosell.mx
Handles photo uploads and folder creation in Google Drive
"""

import os
import json
import pickle
from typing import List, Dict, Optional
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import tempfile

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive.file']

class GoogleDriveService:
    def __init__(self, credentials_file: str = 'credentials_new.json', token_file: str = 'drive_token_new.json'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google Drive API"""
        creds = None
        
        # Load existing token (JSON format)
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, 'r') as token:
                    creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
                print("✅ Loaded existing Google Drive credentials")
            except Exception as e:
                print(f"⚠️ Error loading token file: {e}")
                creds = None
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    print("✅ Refreshed Google Drive credentials")
                except Exception as e:
                    print(f"⚠️ Failed to refresh credentials: {e}")
                    creds = None
            else:
                print("⚠️ No valid Google Drive credentials found")
                print("📝 Photos will be stored locally instead")
                return
            
            # Save credentials for next run
            if creds:
                try:
                    with open(self.token_file, 'w') as token:
                        token.write(creds.to_json())
                    print("💾 Saved Google Drive credentials")
                except Exception as e:
                    print(f"⚠️ Failed to save credentials: {e}")
        
        # Build the service
        if creds and creds.valid:
            try:
                self.service = build('drive', 'v3', credentials=creds)
                print("✅ Google Drive service initialized successfully")
            except Exception as e:
                print(f"❌ Failed to initialize Google Drive service: {e}")
                self.service = None
        else:
            print("⚠️ No valid credentials available for Google Drive")
            self.service = None
    
    def get_or_create_autosell_folder(self) -> str:
        """Get or create the main Autosell.mx folder in Google Drive"""
        if not self.service:
            print("❌ Google Drive service not authenticated")
            return None
        
        try:
            # Search for existing Autosell.mx folder
            query = "name='Autosell.mx' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
            files = results.get('files', [])
            
            if files:
                print(f"✅ Found existing Autosell.mx folder: {files[0]['id']}")
                return files[0]['id']
            
            # Create new Autosell.mx folder
            folder_metadata = {
                'name': 'Autosell.mx',
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = self.service.files().create(body=folder_metadata, fields='id,name').execute()
            print(f"✅ Created main Autosell.mx folder: {folder.get('id')}")
            return folder.get('id')
            
        except Exception as e:
            print(f"❌ Error getting/creating Autosell.mx folder: {e}")
            return None

    def create_folder(self, folder_name: str, parent_folder_id: str = None) -> str:
        """Create a folder in Google Drive"""
        if not self.service:
            print("❌ Google Drive service not authenticated")
            return None
        
        # If no parent specified, use Autosell.mx folder
        if not parent_folder_id:
            parent_folder_id = self.get_or_create_autosell_folder()
            if not parent_folder_id:
                print("❌ Could not get/create Autosell.mx parent folder")
                return None
        
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_folder_id]
        }
        
        try:
            folder = self.service.files().create(
                body=folder_metadata,
                fields='id,name,webViewLink'
            ).execute()
            
            folder_id = folder.get('id')
            folder_url = folder.get('webViewLink')
            print(f"✅ Created folder '{folder_name}' with ID: {folder_id}")
            print(f"🔗 Folder URL: {folder_url}")
            return folder_id
            
        except Exception as e:
            print(f"❌ Error creating folder: {e}")
            return None
    
    def upload_photo(self, file_path: str, folder_id: str, filename: str = None) -> Dict:
        """Upload a photo to Google Drive"""
        if not self.service:
            print("❌ Google Drive service not authenticated")
            return None
        
        if not filename:
            filename = os.path.basename(file_path)
        
        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
        
        try:
            media = MediaFileUpload(file_path, mimetype='image/jpeg')
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink'
            ).execute()
            
            print(f"✅ Uploaded photo '{filename}' with ID: {file.get('id')}")
            return {
                'id': file.get('id'),
                'name': file.get('name'),
                'webViewLink': file.get('webViewLink'),
                'downloadUrl': f"https://drive.google.com/uc?id={file.get('id')}"
            }
            
        except Exception as e:
            print(f"❌ Error uploading photo: {e}")
            return None
    
    def create_vehicle_folder(self, vehicle_id: int, vehicle_name: str) -> str:
        """Create a folder for a specific vehicle"""
        folder_name = f"Vehicle_{vehicle_id}_{vehicle_name}"
        return self.create_folder(folder_name)
    
    def upload_vehicle_photos(self, vehicle_id: int, vehicle_name: str, photos: List[Dict]) -> List[Dict]:
        """Upload multiple photos for a vehicle"""
        # Create vehicle folder
        folder_id = self.create_vehicle_folder(vehicle_id, vehicle_name)
        if not folder_id:
            return []
        
        uploaded_photos = []
        
        for photo in photos:
            # Create temporary file from photo data
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                temp_file.write(photo['content'])
                temp_file_path = temp_file.name
            
            try:
                # Upload to Google Drive
                result = self.upload_photo(
                    temp_file_path, 
                    folder_id, 
                    photo['filename']
                )
                
                if result:
                    uploaded_photos.append({
                        'filename': photo['filename'],
                        'drive_file_id': result['id'],
                        'drive_url': result['webViewLink'],
                        'download_url': result['downloadUrl']
                    })
                
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
        
        return uploaded_photos

# Global instance
drive_service = None

def get_drive_service():
    """Get the global Google Drive service instance"""
    global drive_service
    if drive_service is None:
        drive_service = GoogleDriveService()
    return drive_service

def setup_google_drive():
    """Setup Google Drive integration"""
    print("🔧 Setting up Google Drive integration...")
    
    # Check if credentials file exists
    if not os.path.exists('credentials.json'):
        print("❌ Google Drive credentials not found!")
        print("Please follow these steps:")
        print("1. Go to Google Cloud Console")
        print("2. Create a new project or select existing one")
        print("3. Enable Google Drive API")
        print("4. Create credentials (OAuth 2.0 Client ID)")
        print("5. Download credentials.json to the backend folder")
        return False
    
    # Initialize service
    service = get_drive_service()
    if service and service.service:
        print("✅ Google Drive integration ready!")
        return True
    else:
        print("❌ Google Drive integration failed!")
        return False

if __name__ == "__main__":
    setup_google_drive()
