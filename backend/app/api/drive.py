"""
Google Drive API endpoints for Autosell.mx
Handles Drive folder creation, photo syncing, and file management
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import logging

from ..database import get_db
from ..models.vehicle import Vehicle
from ..models.photo import Photo
from ..services.drive_service import drive_service
from ..schemas.vehicle import VehicleResponse

logger = logging.getLogger(__name__)

router = APIRouter(tags=["drive"])

@router.post("/create-folder/{vehicle_id}")
async def create_vehicle_folder(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    """Create a Google Drive folder for a vehicle"""
    try:
        # Get vehicle information
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        # Create Drive folder
        folder_info = drive_service.create_vehicle_folder(
            vehicle_id=vehicle_id,
            vehicle_info={
                'marca': vehicle.marca or 'Unknown',
                'modelo': vehicle.modelo or 'Unknown',
                'año': vehicle.año or 'Unknown'
            }
        )
        
        if not folder_info:
            raise HTTPException(status_code=500, detail="Failed to create Drive folder")
        
        # Update vehicle with Drive folder information
        vehicle.drive_folder_id = folder_info['folder_id']
        vehicle.drive_folder_url = folder_info['folder_url']
        db.commit()
        
        return {
            "success": True,
            "vehicle_id": vehicle_id,
            "folder_id": folder_info['folder_id'],
            "folder_name": folder_info['folder_name'],
            "folder_url": folder_info['folder_url']
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating Drive folder: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/folder/{folder_id}/files")
async def list_folder_files(folder_id: str):
    """List all files in a Drive folder"""
    try:
        files = drive_service.list_folder_files(folder_id)
        return {
            "success": True,
            "folder_id": folder_id,
            "files": files,
            "count": len(files)
        }
        
    except Exception as e:
        logger.error(f"Error listing Drive folder files: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/sync-photos/{vehicle_id}")
async def sync_vehicle_photos(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    """Sync photos from Drive folder to the system"""
    try:
        # Get vehicle information
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        if not vehicle.drive_folder_id:
            raise HTTPException(status_code=400, detail="Vehicle has no Drive folder")
        
        # Sync photos from Drive
        synced_photos = drive_service.sync_vehicle_photos(
            vehicle_id=vehicle_id,
            folder_id=vehicle.drive_folder_id
        )
        
        # Save photos to database
        saved_photos = []
        for photo_data in synced_photos:
            # Check if photo already exists
            existing_photo = db.query(Photo).filter(
                Photo.vehicle_id == vehicle_id,
                Photo.drive_file_id == photo_data['drive_file_id']
            ).first()
            
            if not existing_photo:
                # Create new photo record
                photo = Photo(
                    vehicle_id=vehicle_id,
                    filename=photo_data['file_name'],
                    file_path=f"drive/{photo_data['drive_file_id']}",  # Store Drive file ID as path
                    file_size=photo_data['file_size'],
                    mime_type=photo_data['mime_type'],
                    drive_file_id=photo_data['drive_file_id'],
                    drive_url=photo_data['drive_url'],
                    is_primary=False
                )
                
                db.add(photo)
                saved_photos.append(photo)
        
        db.commit()
        
        return {
            "success": True,
            "vehicle_id": vehicle_id,
            "synced_photos": len(saved_photos),
            "photos": [
                {
                    "id": photo.id,
                    "filename": photo.filename,
                    "file_size": photo.file_size,
                    "mime_type": photo.mime_type,
                    "drive_url": photo.drive_url
                }
                for photo in saved_photos
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error syncing vehicle photos: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/vehicle/{vehicle_id}/folder-info")
async def get_vehicle_folder_info(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    """Get Drive folder information for a vehicle"""
    try:
        # Get vehicle information
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        if not vehicle.drive_folder_id:
            return {
                "success": True,
                "vehicle_id": vehicle_id,
                "has_folder": False,
                "message": "Vehicle has no Drive folder"
            }
        
        # Get folder files
        files = drive_service.list_folder_files(vehicle.drive_folder_id)
        
        return {
            "success": True,
            "vehicle_id": vehicle_id,
            "has_folder": True,
            "folder_id": vehicle.drive_folder_id,
            "folder_url": vehicle.drive_folder_url,
            "files": files,
            "file_count": len(files)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting vehicle folder info: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/test-connection")
async def test_drive_connection():
    """Test Google Drive API connection"""
    try:
        if drive_service.authenticate():
            return {
                "success": True,
                "message": "Google Drive API connection successful"
            }
        else:
            return {
                "success": False,
                "message": "Google Drive API connection failed"
            }
        
    except Exception as e:
        logger.error(f"Error testing Drive connection: {e}")
        return {
            "success": False,
            "message": f"Connection test failed: {str(e)}"
        }
