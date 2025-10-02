"""
Google Drive Service for Autosell.mx
Handles Drive folder creation, file management, and photo syncing
"""

import os
import json
from typing import Optional, Dict, List, Any
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

logger = logging.getLogger(__name__)

# Google Drive API scopes
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]

class GoogleDriveService:
    """Service for Google Drive operations"""
    
    def __init__(self):
        self.service = None
        self.credentials = None
        self.parent_folder_id = os.getenv('GOOGLE_DRIVE_PARENT_FOLDER_ID')
        
    def authenticate(self) -> bool:
        """Authenticate with Google Drive API"""
        try:
            creds = None
            token_file = 'drive_token.json'
            credentials_file = 'drive_credentials_n8n.json'  # Use n8n credentials
            
            logger.info(f"Starting Google Drive authentication...")
            logger.info(f"Token file: {token_file}")
            logger.info(f"Credentials file: {credentials_file}")
            
            # Load existing credentials
            if os.path.exists(token_file):
                logger.info("Loading existing credentials...")
                creds = Credentials.from_authorized_user_file(token_file, SCOPES)
                logger.info(f"Loaded credentials valid: {creds.valid if creds else False}")
            else:
                logger.info("No existing credentials found")
            
            # If no valid credentials, get new ones
            if not creds or not creds.valid:
                logger.info("No valid credentials, starting OAuth flow...")
                if creds and creds.expired and creds.refresh_token:
                    logger.info("Refreshing expired credentials...")
                    creds.refresh(Request())
                else:
                    if not os.path.exists(credentials_file):
                        logger.error(f"Google Drive credentials file not found: {credentials_file}")
                        return False
                    
                    logger.info("Starting OAuth flow with redirect URI: http://localhost:8081/")
                    # Use fixed redirect URI approach
                    flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                    # Use a completely fixed redirect URI
                    flow.redirect_uri = 'http://localhost:8081/'
                    creds = flow.run_local_server(port=8081, redirect_uri_trailing_slash=False)
                    logger.info("OAuth flow completed successfully")
                
                # Save credentials for next run
                logger.info("Saving credentials...")
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
                logger.info("Credentials saved successfully")
            
            logger.info("Building Drive service...")
            self.credentials = creds
            self.service = build('drive', 'v3', credentials=creds)
            logger.info("Google Drive authentication successful!")
            return True
            
        except Exception as e:
            logger.error(f"Google Drive authentication failed: {e}")
            logger.error(f"Exception type: {type(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
    
    def create_vehicle_folder(self, vehicle_id: int, vehicle_info: Dict[str, Any]) -> Optional[Dict[str, str]]:
        """Create a Drive folder for a vehicle"""
        try:
            if not self.service:
                if not self.authenticate():
                    return None
            
            # Create folder name
            folder_name = f"Vehicle-{vehicle_id}-{vehicle_info.get('marca', 'Unknown')}-{vehicle_info.get('modelo', 'Unknown')}"
            
            # Create folder metadata
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            # Only add parent if it's configured
            if self.parent_folder_id:
                folder_metadata['parents'] = [self.parent_folder_id]
            
            # Create the folder
            logger.info(f"Creating Drive folder: {folder_name}")
            logger.info(f"Folder metadata: {folder_metadata}")
            
            folder = self.service.files().create(
                body=folder_metadata,
                fields='id,name,webViewLink'
            ).execute()
            
            logger.info(f"Drive folder created successfully: {folder['id']}")
            
            # Make folder shareable
            permission = {
                'type': 'anyone',
                'role': 'reader'
            }
            
            self.service.permissions().create(
                fileId=folder['id'],
                body=permission
            ).execute()
            
            logger.info(f"Drive folder permissions set successfully")
            
            return {
                'folder_id': folder['id'],
                'folder_name': folder['name'],
                'folder_url': folder['webViewLink']
            }
            
        except HttpError as e:
            logger.error(f"Google Drive API error: {e}")
            logger.error(f"API error details: {e.error_details}")
            logger.error(f"API error reason: {e.reason}")
            return None
        except Exception as e:
            logger.error(f"Error creating Drive folder: {e}")
            logger.error(f"Exception type: {type(e)}")
            logger.error(f"Exception details: {str(e)}")
            return None
    
    def list_folder_files(self, folder_id: str) -> List[Dict[str, Any]]:
        """List all files in a Drive folder"""
        try:
            if not self.service:
                if not self.authenticate():
                    return []
            
            # Query for files in the folder
            query = f"'{folder_id}' in parents and trashed=false"
            results = self.service.files().list(
                q=query,
                fields="files(id,name,mimeType,size,createdTime,webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            
            # Filter for image files
            image_files = []
            for file in files:
                mime_type = file.get('mimeType', '')
                if mime_type.startswith('image/'):
                    image_files.append({
                        'id': file['id'],
                        'name': file['name'],
                        'mime_type': mime_type,
                        'size': file.get('size', 0),
                        'created_time': file.get('createdTime', ''),
                        'url': file.get('webViewLink', '')
                    })
            
            return image_files
            
        except HttpError as e:
            logger.error(f"Google Drive API error listing files: {e}")
            return []
        except Exception as e:
            logger.error(f"Error listing Drive folder files: {e}")
            return []
    
    def download_file(self, file_id: str) -> Optional[bytes]:
        """Download a file from Drive"""
        try:
            if not self.service:
                if not self.authenticate():
                    return None
            
            # Download file content
            request = self.service.files().get_media(fileId=file_id)
            file_content = request.execute()
            
            return file_content
            
        except HttpError as e:
            logger.error(f"Google Drive API error downloading file: {e}")
            return None
        except Exception as e:
            logger.error(f"Error downloading Drive file: {e}")
            return None
    
    def get_file_info(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Get file information from Drive"""
        try:
            if not self.service:
                if not self.authenticate():
                    return None
            
            file_info = self.service.files().get(
                fileId=file_id,
                fields="id,name,mimeType,size,createdTime,webViewLink"
            ).execute()
            
            return {
                'id': file_info['id'],
                'name': file_info['name'],
                'mime_type': file_info.get('mimeType', ''),
                'size': file_info.get('size', 0),
                'created_time': file_info.get('createdTime', ''),
                'url': file_info.get('webViewLink', '')
            }
            
        except HttpError as e:
            logger.error(f"Google Drive API error getting file info: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting Drive file info: {e}")
            return None
    
    def sync_vehicle_photos(self, vehicle_id: int, folder_id: str) -> List[Dict[str, Any]]:
        """Sync photos from Drive folder to the system"""
        try:
            # Get all files in the folder
            files = self.list_folder_files(folder_id)
            
            synced_photos = []
            for file in files:
                # Download file content
                file_content = self.download_file(file['id'])
                if file_content:
                    synced_photos.append({
                        'vehicle_id': vehicle_id,
                        'drive_file_id': file['id'],
                        'file_name': file['name'],
                        'mime_type': file['mime_type'],
                        'file_size': file['size'],
                        'file_content': file_content,
                        'drive_url': file['url']
                    })
            
            return synced_photos
            
        except Exception as e:
            logger.error(f"Error syncing vehicle photos: {e}")
            return []

# Global instance
drive_service = GoogleDriveService()
