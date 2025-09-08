#!/usr/bin/env python3
"""
Photo Model
Defines the Photo database model and Pydantic schemas
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from ..database import Base

class Photo(Base):
    """Photo database model"""
    __tablename__ = "photos"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=True)
    drive_url = Column(Text, nullable=True)
    drive_file_id = Column(String(255), nullable=True, index=True)
    order_index = Column(Integer, default=0)
    is_primary = Column(Boolean, default=False)
    file_size = Column(Integer, nullable=True)
    mime_type = Column(String(100), nullable=True)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    vehicle = relationship("Vehicle", back_populates="photos")
    
    def __repr__(self):
        return f"<Photo(id={self.id}, vehicle_id={self.vehicle_id}, file_name='{self.file_name}')>"

# Pydantic schemas
class PhotoBase(BaseModel):
    """Base photo schema"""
    vehicle_id: int = Field(..., description="ID of the vehicle this photo belongs to")
    filename: str = Field(..., description="Name of the photo file")
    original_filename: Optional[str] = Field(None, description="Original filename")
    drive_url: Optional[str] = Field(None, description="Google Drive view URL")
    drive_file_id: Optional[str] = Field(None, description="Google Drive file ID")
    order_index: int = Field(0, description="Order index for photo display")
    is_primary: bool = Field(False, description="Whether this is the primary photo for the vehicle")
    file_size: Optional[int] = Field(None, description="Size of the file in bytes")
    mime_type: Optional[str] = Field(None, description="MIME type of the file")
    width: Optional[int] = Field(None, description="Photo width in pixels")
    height: Optional[int] = Field(None, description="Photo height in pixels")

class PhotoCreate(PhotoBase):
    """Schema for creating a new photo"""
    pass

class PhotoUpdate(BaseModel):
    """Schema for updating a photo"""
    filename: Optional[str] = Field(None, description="Name of the photo file")
    original_filename: Optional[str] = Field(None, description="Original filename")
    drive_url: Optional[str] = Field(None, description="Google Drive view URL")
    drive_file_id: Optional[str] = Field(None, description="Google Drive file ID")
    order_index: Optional[int] = Field(None, description="Order index for photo display")
    is_primary: Optional[bool] = Field(None, description="Whether this is the primary photo")
    file_size: Optional[int] = Field(None, description="Size of the file in bytes")
    mime_type: Optional[str] = Field(None, description="MIME type of the file")
    width: Optional[int] = Field(None, description="Photo width in pixels")
    height: Optional[int] = Field(None, description="Photo height in pixels")

class PhotoResponse(PhotoBase):
    """Schema for photo responses"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class PhotoListResponse(BaseModel):
    """Schema for photo list responses"""
    photos: list[PhotoResponse]
    total: int
    vehicle_id: int

class PhotoStats(BaseModel):
    """Schema for photo statistics"""
    total_photos: int
    total_size_bytes: int
    total_size_mb: float
    vehicles_with_photos: int
    average_photos_per_vehicle: float
    primary_photos: int

class GoogleDriveSyncResponse(BaseModel):
    """Schema for Google Drive sync responses"""
    total_files: int
    synced_count: int
    new_count: int
