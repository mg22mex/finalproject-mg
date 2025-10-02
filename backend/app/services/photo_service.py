#!/usr/bin/env python3
"""
Photo Management Service
Handles Google Drive integration, photo storage, and vehicle-photo associations
"""

import os
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path
import mimetypes
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError
import io
from PIL import Image
import hashlib

from ..database import get_db
from ..models.photo import Photo, PhotoCreate, PhotoUpdate
from ..models.vehicle import Vehicle

logger = logging.getLogger(__name__)

# Google Drive API scopes
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]

class PhotoService:
    """Service for managing photos and Google Drive integration"""
    
    def __init__(self):
        self.credentials = None
        self.service = None
        self.folder_id = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Drive API"""
        try:
            # Check if we have valid credentials
            if os.path.exists('token.json'):
                self.credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
            
            # If no valid credentials available, let the user log in
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    self.credentials.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'drive_credentials_n8n.json', SCOPES)
                    # Use fixed redirect URI
                    flow.redirect_uri = 'http://localhost:8081/'
                    self.credentials = flow.run_local_server(port=8081, redirect_uri_trailing_slash=False)
                
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(self.credentials.to_json())
            
            # Build the service
            self.service = build('drive', 'v3', credentials=self.credentials)
            
            # Get or create the main folder
            self.folder_id = self._get_or_create_main_folder()
            
            logger.info("Google Drive authentication successful")
            
        except Exception as e:
            logger.error(f"Google Drive authentication failed: {e}")
            self.service = None
    
    def _get_or_create_main_folder(self) -> Optional[str]:
        """Get or create the main Autosell.mx folder in Google Drive"""
        try:
            # Search for existing folder
            query = "name='Autosell.mx' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
            files = results.get('files', [])
            
            if files:
                return files[0]['id']
            
            # Create new folder
            folder_metadata = {
                'name': 'Autosell.mx',
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = self.service.files().create(body=folder_metadata, fields='id').execute()
            logger.info(f"Created main folder: {folder.get('id')}")
            return folder.get('id')
            
        except Exception as e:
            logger.error(f"Failed to get/create main folder: {e}")
            return None
    
    def _get_or_create_vehicle_folder(self, vehicle_id: int, vehicle_name: str) -> Optional[str]:
        """Get or create a folder for a specific vehicle"""
        try:
            folder_name = f"{vehicle_id}_{vehicle_name}"
            
            # Search for existing vehicle folder
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{self.folder_id}' in parents and trashed=false"
            results = self.service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
            files = results.get('files', [])
            
            if files:
                return files[0]['id']
            
            # Create new vehicle folder
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [self.folder_id]
            }
            folder = self.service.files().create(body=folder_metadata, fields='id').execute()
            logger.info(f"Created vehicle folder: {folder.get('id')}")
            return folder.get('id')
            
        except Exception as e:
            logger.error(f"Failed to get/create vehicle folder: {e}")
            return None
    
    async def upload_photo(self, vehicle_id: int, file_path: str, description: str = None) -> Optional[Photo]:
        """Upload a photo to Google Drive and create database record"""
        try:
            if not self.service:
                raise Exception("Google Drive service not available")
            
            # Get vehicle info
            db = next(get_db())
            vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
            if not vehicle:
                raise Exception(f"Vehicle {vehicle_id} not found")
            
            # Create vehicle folder
            vehicle_folder_id = self._get_or_create_vehicle_folder(
                vehicle_id, 
                f"{vehicle.marca}_{vehicle.modelo}_{vehicle.año}"
            )
            
            if not vehicle_folder_id:
                raise Exception("Failed to create vehicle folder")
            
            # Prepare file metadata
            file_name = Path(file_path).name
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = 'application/octet-stream'
            
            # Upload file to Google Drive
            file_metadata = {
                'name': file_name,
                'parents': [vehicle_folder_id],
                'description': description or f"Photo for {vehicle.marca} {vehicle.modelo} {vehicle.año}"
            }
            
            media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,size,webViewLink,thumbnailLink'
            ).execute()
            
            # Note: Thumbnail generation removed for simplicity
            # Can be re-implemented later if needed
            
            # Create database record
            photo_data = PhotoCreate(
                vehicle_id=vehicle_id,
                filename=file_name,
                original_filename=file_name,
                drive_url=file.get('webViewLink'),
                drive_file_id=file.get('id'),
                file_size=file.get('size', 0),
                mime_type=mime_type,
                width=file.get('imageMediaMetadata', {}).get('width') if 'imageMediaMetadata' in file else None,
                height=file.get('imageMediaMetadata', {}).get('height') if 'imageMediaMetadata' in file else None
            )
            
            photo = Photo(**photo_data.dict())
            db.add(photo)
            db.commit()
            db.refresh(photo)
            
            logger.info(f"Photo uploaded successfully: {file.get('id')}")
            return photo
            
        except Exception as e:
            logger.error(f"Failed to upload photo: {e}")
            return None
    
    async def get_vehicle_photos(self, vehicle_id: int) -> List[Photo]:
        """Get all photos for a specific vehicle"""
        try:
            db = next(get_db())
            photos = db.query(Photo).filter(Photo.vehicle_id == vehicle_id).order_by(Photo.created_at.desc()).all()
            return photos
        except Exception as e:
            logger.error(f"Failed to get vehicle photos: {e}")
            return []
    
    async def delete_photo(self, photo_id: int) -> bool:
        """Delete a photo from both Google Drive and database"""
        try:
            db = next(get_db())
            photo = db.query(Photo).filter(Photo.id == photo_id).first()
            
            if not photo:
                return False
            
            # Delete from Google Drive
            if self.service and photo.drive_file_id:
                try:
                    self.service.files().delete(fileId=photo.drive_file_id).execute()
                    logger.info(f"Deleted photo from Google Drive: {photo.drive_file_id}")
                except Exception as e:
                    logger.warning(f"Failed to delete from Google Drive: {e}")
            
            # Delete from database
            db.delete(photo)
            db.commit()
            
            logger.info(f"Photo deleted successfully: {photo_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete photo: {e}")
            return False
    
    async def update_photo_description(self, photo_id: int, filename: str) -> Optional[Photo]:
        """Update photo filename"""
        try:
            db = next(get_db())
            photo = db.query(Photo).filter(Photo.id == photo_id).first()
            
            if not photo:
                return None
            
            photo.filename = filename
            photo.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(photo)
            
            return photo
            
        except Exception as e:
            logger.error(f"Failed to update photo filename: {e}")
            return None
    
    async def get_photo_stats(self) -> Dict[str, Any]:
        """Get photo statistics"""
        try:
            db = next(get_db())
            
            total_photos = db.query(Photo).count()
            total_size = db.query(Photo.file_size).all()
            total_size_bytes = sum(size[0] for size in total_size if size[0])
            
            # Group by vehicle
            vehicle_photo_counts = db.query(
                Photo.vehicle_id,
                db.func.count(Photo.id).label('photo_count')
            ).group_by(Photo.vehicle_id).all()
            
            # Count primary photos
            primary_photos = db.query(Photo).filter(Photo.is_primary == True).count()
            
            stats = {
                'total_photos': total_photos,
                'total_size_bytes': total_size_bytes,
                'total_size_mb': round(total_size_bytes / (1024 * 1024), 2),
                'vehicles_with_photos': len(vehicle_photo_counts),
                'average_photos_per_vehicle': round(total_photos / len(vehicle_photo_counts), 2) if vehicle_photo_counts else 0,
                'primary_photos': primary_photos
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get photo stats: {e}")
            return {}
    
    async def sync_google_drive_photos(self) -> Dict[str, Any]:
        """Sync photos from Google Drive to database"""
        try:
            if not self.service:
                raise Exception("Google Drive service not available")
            
            # Get all files from the main folder
            results = self.service.files().list(
                q=f"'{self.folder_id}' in parents and trashed=false",
                fields="files(id,name,mimeType,size,webViewLink,createdTime,parents)",
                pageSize=1000
            ).execute()
            
            files = results.get('files', [])
            synced_count = 0
            new_count = 0
            
            for file in files:
                if file['mimeType'].startswith('image/'):
                    # Check if photo already exists in database
                    db = next(get_db())
                    existing_photo = db.query(Photo).filter(
                        Photo.drive_file_id == file['id']
                    ).first()
                    
                    if not existing_photo:
                        # Try to determine vehicle from folder structure
                        vehicle_id = self._extract_vehicle_id_from_parents(file.get('parents', []))
                        
                        if vehicle_id:
                            # Create new photo record
                            photo_data = PhotoCreate(
                                vehicle_id=vehicle_id,
                                filename=file['name'],
                                original_filename=file['name'],
                                drive_url=file.get('webViewLink'),
                                drive_file_id=file['id'],
                                file_size=int(file.get('size', 0)),
                                mime_type=file['mimeType'],
                                width=file.get('imageMediaMetadata', {}).get('width') if 'imageMediaMetadata' in file else None,
                                height=file.get('imageMediaMetadata', {}).get('height') if 'imageMediaMetadata' in file else None
                            )
                            
                            photo = Photo(**photo_data.dict())
                            db.add(photo)
                            new_count += 1
                    
                    synced_count += 1
            
            db.commit()
            
            return {
                'total_files': len(files),
                'synced_count': synced_count,
                'new_count': new_count
            }
            
        except Exception as e:
            logger.error(f"Failed to sync Google Drive photos: {e}")
            return {}
    
    def _extract_vehicle_id_from_parents(self, parent_ids: List[str]) -> Optional[int]:
        """Extract vehicle ID from parent folder name"""
        try:
            for parent_id in parent_ids:
                # Get parent folder info
                parent = self.service.files().get(fileId=parent_id, fields='name').execute()
                folder_name = parent.get('name', '')
                
                # Extract vehicle ID from folder name (format: "123_Toyota_Camry_2020")
                if '_' in folder_name:
                    vehicle_id_str = folder_name.split('_')[0]
                    try:
                        return int(vehicle_id_str)
                    except ValueError:
                        continue
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to extract vehicle ID from parents: {e}")
            return None

# Global instance
photo_service = PhotoService()
