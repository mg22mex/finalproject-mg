"""
Photos API endpoints - Basic photo management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.photo import Photo

# Create router
router = APIRouter(prefix="/photos", tags=["photos"])

@router.get("/")
async def get_photos(db: Session = Depends(get_db)):
    """Get all photos"""
    try:
        photos = db.query(Photo).all()
        return {"photos": [{
            "id": photo.id,
            "vehicle_id": photo.vehicle_id,
            "filename": photo.filename,
            "original_filename": photo.original_filename,
            "drive_url": photo.drive_url,
            "drive_file_id": photo.drive_file_id,
            "order_index": photo.order_index,
            "is_primary": photo.is_primary,
            "file_size": photo.file_size,
            "mime_type": photo.mime_type,
            "width": photo.width,
            "height": photo.height,
            "created_at": photo.created_at,
            "updated_at": photo.updated_at
        } for photo in photos]}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/{photo_id}")
async def get_photo(photo_id: int, db: Session = Depends(get_db)):
    """Get a specific photo"""
    try:
        photo = db.query(Photo).filter(Photo.id == photo_id).first()
        if not photo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Photo not found"
            )
        return {
            "id": photo.id,
            "vehicle_id": photo.vehicle_id,
            "filename": photo.filename,
            "original_filename": photo.original_filename,
            "drive_url": photo.drive_url,
            "drive_file_id": photo.drive_file_id,
            "order_index": photo.order_index,
            "is_primary": photo.is_primary,
            "file_size": photo.file_size,
            "mime_type": photo.mime_type,
            "width": photo.width,
            "height": photo.height,
            "created_at": photo.created_at,
            "updated_at": photo.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
