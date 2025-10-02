#!/usr/bin/env python3
"""
Photo API Endpoints
Handles photo management, Google Drive integration, and vehicle-photo associations
"""

import os
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import tempfile
import shutil

from ...database import get_db
from ...models.photo import Photo, PhotoCreate, PhotoUpdate, PhotoResponse, PhotoListResponse, PhotoStats, GoogleDriveSyncResponse
from ...models.vehicle import Vehicle
from ...services.photo_service import photo_service
# from ...core.config import settings  # Not used yet

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[PhotoResponse])
async def get_photos(
    vehicle_id: Optional[int] = Query(None, description="Filter by vehicle ID"),
    is_primary: Optional[bool] = Query(None, description="Filter by primary photo status"),
    is_active: Optional[bool] = Query(True, description="Filter by active status"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    db: Session = Depends(get_db)
):
    """Get all photos with optional filtering"""
    try:
        query = db.query(Photo)
        
        if vehicle_id is not None:
            query = query.filter(Photo.vehicle_id == vehicle_id)
        
        if is_primary is not None:
            query = query.filter(Photo.is_primary == is_primary)
        
        # Note: is_active field doesn't exist in Photo model, so we skip this filter
        
        photos = query.offset(skip).limit(limit).all()
        return photos
        
    except Exception as e:
        logger.error(f"Failed to get photos: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve photos")

@router.get("/vehicle/{vehicle_id}", response_model=PhotoListResponse)
async def get_vehicle_photos(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    """Get all photos for a specific vehicle"""
    try:
        # Verify vehicle exists
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        photos = await photo_service.get_vehicle_photos(vehicle_id)
        
        return PhotoListResponse(
            photos=photos,
            total=len(photos),
            vehicle_id=vehicle_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get vehicle photos: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve vehicle photos")

@router.get("/{photo_id}", response_model=PhotoResponse)
async def get_photo(
    photo_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific photo by ID"""
    try:
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
        if not photo:
            raise HTTPException(status_code=404, detail="Photo not found")
        
        return photo
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get photo: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve photo")

@router.post("/upload/{vehicle_id}", response_model=PhotoResponse)
async def upload_photo(
    vehicle_id: int,
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Upload a photo for a specific vehicle with Google Drive integration"""
    try:
        # Verify vehicle exists
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Only image files are allowed")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_file_path = temp_file.name
        
        try:
            # Import Drive service
            from ...services.drive_service import drive_service
            
            # Ensure vehicle has a Drive folder
            if not vehicle.drive_folder_id:
                # Create Drive folder for vehicle
                folder_info = drive_service.create_vehicle_folder(
                    vehicle_id, 
                    {
                        'marca': vehicle.marca,
                        'modelo': vehicle.modelo,
                        'año': vehicle.año
                    }
                )
                
                if folder_info:
                    vehicle.drive_folder_id = folder_info['folder_id']
                    vehicle.drive_folder_url = folder_info['folder_url']
                    db.commit()
                else:
                    raise HTTPException(status_code=500, detail="Failed to create Drive folder")
            
            # Upload photo to Google Drive
            with open(temp_file_path, 'rb') as f:
                file_content = f.read()
            
            drive_result = drive_service.upload_photo_to_vehicle_folder(
                vehicle_id=vehicle_id,
                folder_id=vehicle.drive_folder_id,
                file_content=file_content,
                filename=file.filename,
                mime_type=file.content_type
            )
            
            if not drive_result:
                raise HTTPException(status_code=500, detail="Failed to upload photo to Google Drive")
            
            # Create photo record in database (metadata only)
            photo = Photo(
                vehicle_id=vehicle_id,
                filename=drive_result['filename'],
                original_filename=file.filename,
                drive_file_id=drive_result['drive_file_id'],
                drive_url=drive_result['drive_url'],
                file_size=drive_result['file_size'],
                mime_type=file.content_type,
                is_primary=False,
                order_index=0
            )
            
            db.add(photo)
            db.commit()
            db.refresh(photo)
            
            logger.info(f"Photo uploaded successfully to Drive: {photo.id}")
            return photo
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to upload photo: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload photo")

@router.put("/{photo_id}", response_model=PhotoResponse)
async def update_photo(
    photo_id: int,
    photo_update: PhotoUpdate,
    db: Session = Depends(get_db)
):
    """Update photo information"""
    try:
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
        if not photo:
            raise HTTPException(status_code=404, detail="Photo not found")
        
        # Update fields
        update_data = photo_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(photo, field, value)
        
        # Handle primary photo logic
        if photo_update.is_primary:
            # Unset other primary photos for this vehicle
            other_photos = db.query(Photo).filter(
                Photo.vehicle_id == photo.vehicle_id,
                Photo.id != photo_id,
                Photo.is_primary == True
            ).all()
            
            for other_photo in other_photos:
                other_photo.is_primary = False
        
        db.commit()
        db.refresh(photo)
        
        return photo
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update photo: {e}")
        raise HTTPException(status_code=500, detail="Failed to update photo")

@router.delete("/{photo_id}")
async def delete_photo(
    photo_id: int,
    db: Session = Depends(get_db)
):
    """Delete a photo"""
    try:
        success = await photo_service.delete_photo(photo_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Photo not found")
        
        return {"message": "Photo deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete photo: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete photo")

@router.get("/stats/overview", response_model=PhotoStats)
async def get_photo_stats():
    """Get photo statistics overview"""
    try:
        stats = await photo_service.get_photo_stats()
        return PhotoStats(**stats)
        
    except Exception as e:
        logger.error(f"Failed to get photo stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve photo statistics")

@router.post("/sync/google-drive", response_model=GoogleDriveSyncResponse)
async def sync_google_drive_photos():
    """Sync photos from Google Drive to database"""
    try:
        sync_result = await photo_service.sync_google_drive_photos()
        return GoogleDriveSyncResponse(**sync_result)
        
    except Exception as e:
        logger.error(f"Failed to sync Google Drive photos: {e}")
        raise HTTPException(status_code=500, detail="Failed to sync Google Drive photos")

@router.get("/vehicle/{vehicle_id}/primary", response_model=PhotoResponse)
async def get_primary_photo(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    """Get the primary photo for a specific vehicle"""
    try:
        # Verify vehicle exists
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        # Get primary photo
        primary_photo = db.query(Photo).filter(
            Photo.vehicle_id == vehicle_id,
            Photo.is_primary == True,
            Photo.is_active == True
        ).first()
        
        if not primary_photo:
            raise HTTPException(status_code=404, detail="No primary photo found for this vehicle")
        
        return primary_photo
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get primary photo: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve primary photo")

@router.post("/vehicle/{vehicle_id}/photos/{photo_id}/set-primary")
async def set_primary_photo(
    vehicle_id: int,
    photo_id: int,
    db: Session = Depends(get_db)
):
    """Set a photo as the primary photo for a vehicle"""
    try:
        # Verify vehicle exists
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        # Verify photo exists and belongs to vehicle
        photo = db.query(Photo).filter(
            Photo.id == photo_id,
            Photo.vehicle_id == vehicle_id
        ).first()
        
        if not photo:
            raise HTTPException(status_code=404, detail="Photo not found")
        
        # Unset other primary photos for this vehicle
        other_primary_photos = db.query(Photo).filter(
            Photo.vehicle_id == vehicle_id,
            Photo.id != photo_id,
            Photo.is_primary == True
        ).all()
        
        for other_photo in other_primary_photos:
            other_photo.is_primary = False
        
        # Set this photo as primary
        photo.is_primary = True
        
        db.commit()
        
        return {"message": "Primary photo updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to set primary photo: {e}")
        raise HTTPException(status_code=500, detail="Failed to set primary photo")

@router.get("/search", response_model=List[PhotoResponse])
async def search_photos(
    query: str = Query(..., description="Search term for photo descriptions or filenames"),
    vehicle_id: Optional[int] = Query(None, description="Filter by vehicle ID"),
    db: Session = Depends(get_db)
):
    """Search photos by description or filename"""
    try:
        search_query = db.query(Photo)
        
        if vehicle_id:
            search_query = search_query.filter(Photo.vehicle_id == vehicle_id)
        
        # Search in filename and original filename
        search_query = search_query.filter(
            db.or_(
                Photo.filename.ilike(f"%{query}%"),
                Photo.original_filename.ilike(f"%{query}%")
            )
        )
        
        photos = search_query.all()
        return photos
        
    except Exception as e:
        logger.error(f"Failed to search photos: {e}")
        raise HTTPException(status_code=500, detail="Failed to search photos")

@router.post("/vehicle/{vehicle_id}/sync-drive")
async def sync_vehicle_drive_photos(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    """Sync photos from Google Drive folder to database"""
    try:
        # Verify vehicle exists
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        if not vehicle.drive_folder_id:
            raise HTTPException(status_code=400, detail="Vehicle has no Drive folder")
        
        # Import Drive service
        from ...services.drive_service import drive_service
        
        # Sync photos from Drive
        drive_photos = drive_service.sync_vehicle_photos(vehicle_id, vehicle.drive_folder_id)
        
        synced_count = 0
        new_count = 0
        
        for drive_photo in drive_photos:
            # Check if photo already exists
            existing_photo = db.query(Photo).filter(
                Photo.drive_file_id == drive_photo['drive_file_id']
            ).first()
            
            if not existing_photo:
                # Create new photo record
                photo = Photo(
                    vehicle_id=vehicle_id,
                    filename=drive_photo['filename'],
                    drive_file_id=drive_photo['drive_file_id'],
                    drive_url=drive_photo['drive_url'],
                    file_size=drive_photo['file_size'],
                    mime_type=drive_photo['mime_type'],
                    is_primary=False,
                    order_index=0
                )
                
                db.add(photo)
                new_count += 1
            
            synced_count += 1
        
        db.commit()
        
        return {
            "message": "Drive photos synced successfully",
            "total_files": len(drive_photos),
            "synced_count": synced_count,
            "new_count": new_count
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to sync Drive photos: {e}")
        raise HTTPException(status_code=500, detail="Failed to sync Drive photos")

@router.get("/vehicle/{vehicle_id}/drive-folder")
async def get_vehicle_drive_folder(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    """Get vehicle's Google Drive folder information"""
    try:
        # Verify vehicle exists
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        if not vehicle.drive_folder_id:
            return {
                "has_folder": False,
                "message": "Vehicle has no Drive folder"
            }
        
        # Import Drive service
        from ...services.drive_service import drive_service
        
        # Get folder files
        files = drive_service.list_folder_files(vehicle.drive_folder_id)
        
        return {
            "has_folder": True,
            "folder_id": vehicle.drive_folder_id,
            "folder_url": vehicle.drive_folder_url,
            "files": files,
            "file_count": len(files)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get Drive folder info: {e}")
        raise HTTPException(status_code=500, detail="Failed to get Drive folder info")

@router.get("/{photo_id}/thumbnail")
async def get_photo_thumbnail(
    photo_id: int,
    size: str = Query("medium", description="Thumbnail size: small, medium, large"),
    db: Session = Depends(get_db)
):
    """Get photo thumbnail URL from Google Drive"""
    try:
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
        if not photo:
            raise HTTPException(status_code=404, detail="Photo not found")
        
        if not photo.drive_file_id:
            raise HTTPException(status_code=400, detail="Photo has no Drive file ID")
        
        # Import Drive service
        from ...services.drive_service import drive_service
        
        thumbnail_url = drive_service.get_photo_thumbnail_url(photo.drive_file_id, size)
        
        if not thumbnail_url:
            raise HTTPException(status_code=500, detail="Failed to generate thumbnail URL")
        
        return {
            "thumbnail_url": thumbnail_url,
            "direct_url": drive_service.get_photo_direct_url(photo.drive_file_id),
            "drive_url": photo.drive_url
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get photo thumbnail: {e}")
        raise HTTPException(status_code=500, detail="Failed to get photo thumbnail")
