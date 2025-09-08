"""
Vehicle Model - Core entity for the vehicle management system
"""

from sqlalchemy import Column, Integer, String, Numeric, Text, DateTime, JSON, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, List
import enum

from ..database import Base

class VehicleStatus(str, enum.Enum):
    """Vehicle status enumeration"""
    DISPONIBLE = "DISPONIBLE"
    FOTOS = "FOTOS"
    AUSENTE = "AUSENTE"
    APARTADO = "APARTADO"
    VENDIDO = "VENDIDO"

class Vehicle(Base):
    """Vehicle model representing a vehicle in the system"""
    
    __tablename__ = "vehicles"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # External identifier (from Google Sheets)
    external_id = Column(String(100), unique=True, index=True)
    
    # Basic vehicle information
    marca = Column(String(100), nullable=False, index=True)
    modelo = Column(String(100), nullable=False, index=True)
    año = Column(Integer, nullable=False, index=True)
    color = Column(String(50))
    precio = Column(Numeric(12, 2), index=True)
    kilometraje = Column(String(50))
    
    # Status and location
    estatus = Column(Enum(VehicleStatus, name='vehicle_status'), default=VehicleStatus.DISPONIBLE, index=True)
    ubicacion = Column(String(100))
    
    # Additional information
    descripcion = Column(Text)
    caracteristicas = Column(JSON)  # Additional features as JSON
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(String(100))
    updated_by = Column(String(100))
    
    # Relationships
    photos = relationship("Photo", back_populates="vehicle", cascade="all, delete-orphan")
    social_posts = relationship("SocialPost", back_populates="vehicle", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Vehicle(id={self.id}, marca='{self.marca}', modelo='{self.modelo}', año={self.año})>"
    
    @property
    def display_name(self) -> str:
        """Get display name for the vehicle"""
        return f"{self.año} {self.marca} {self.modelo}"
    
    @property
    def is_available(self) -> bool:
        """Check if vehicle is available for sale"""
        return self.estatus in [VehicleStatus.DISPONIBLE, VehicleStatus.FOTOS]
    
    @property
    def is_sold(self) -> bool:
        """Check if vehicle is sold"""
        return self.estatus == VehicleStatus.VENDIDO
    
    @property
    def is_reserved(self) -> bool:
        """Check if vehicle is reserved"""
        return self.estatus == VehicleStatus.APARTADO
    
    @property
    def is_temporarily_unavailable(self) -> bool:
        """Check if vehicle is temporarily unavailable"""
        return self.estatus == VehicleStatus.AUSENTE
    
    def update_status(self, new_status: VehicleStatus, changed_by: str, reason: str = None, notes: str = None):
        """Update vehicle status and record in history"""
        old_status = self.estatus
        self.estatus = new_status
        self.updated_by = changed_by
        
        # TODO: Create status history record when relationships are working
        return None
    
    def get_primary_photo(self):
        """Get the primary photo for this vehicle"""
        if hasattr(self, 'photos'):
            for photo in self.photos:
                if photo.is_primary and photo.is_active:
                    return photo
        return None
    
    def get_photo_count(self) -> int:
        """Get total number of photos"""
        if hasattr(self, 'photos'):
            return len([p for p in self.photos if p.is_active])
        return 0
    
    def get_active_social_posts(self):
        """Get active social media posts"""
        # TODO: Implement when relationships are working
        return []
    
    def get_active_marketplace_listings(self):
        """Get active marketplace listings"""
        # TODO: Implement when relationships are working
        return []
    
    def to_dict(self) -> dict:
        """Convert vehicle to dictionary for API responses"""
        return {
            "id": self.id,
            "external_id": self.external_id,
            "marca": self.marca,
            "modelo": self.modelo,
            "año": self.año,
            "color": self.color,
            "precio": float(self.precio) if self.precio else None,
            "kilometraje": self.kilometraje,
            "estatus": self.estatus.value if self.estatus else None,
            "ubicacion": self.ubicacion,
            "descripcion": self.descripcion,
            "caracteristicas": self.caracteristicas,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "created_by": self.created_by,
            "updated_by": self.updated_by,
            "photo_count": self.get_photo_count(),
            "is_available": self.is_available,
            "is_sold": self.is_sold,
            "is_reserved": self.is_reserved,
            "is_temporarily_unavailable": self.is_temporarily_unavailable
        }
    
    @classmethod
    def from_google_sheets(cls, row_data: dict) -> 'Vehicle':
        """Create vehicle from Google Sheets data"""
        return cls(
            external_id=row_data.get('#'),
            marca=row_data.get('Marca'),
            modelo=row_data.get('Modelo'),
            año=int(row_data.get('Año', 0)),
            color=row_data.get('Color'),
            precio=float(row_data.get('# Precio', 0)) if row_data.get('# Precio') else None,
            kilometraje=row_data.get('# km'),
            estatus=VehicleStatus(row_data.get('Estatus', 'Disponible')),
            ubicacion=row_data.get('Ubicacion'),
            descripcion=row_data.get('Descripcion'),
            caracteristicas={
                'grupo': row_data.get('GRUPO'),
                'fecha': row_data.get('Column 2'),
                'fotos': row_data.get('Fotos')
            }
        )
