"""
Vehicle Pydantic Schemas - Data validation and serialization
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class VehicleStatus(str, Enum):
    """Vehicle status enumeration for API"""
    DISPONIBLE = "DISPONIBLE"
    FOTOS = "FOTOS"
    AUSENTE = "AUSENTE"
    APARTADO = "APARTADO"
    VENDIDO = "VENDIDO"

class VehicleBase(BaseModel):
    """Base vehicle schema with common fields"""
    
    external_id: Optional[str] = Field(None, max_length=100, description="External identifier from Google Sheets")
    marca: str = Field(..., max_length=100, description="Vehicle brand")
    modelo: str = Field(..., max_length=100, description="Vehicle model")
    año: int = Field(..., ge=1900, le=2030, description="Vehicle year")
    color: Optional[str] = Field(None, max_length=50, description="Vehicle color")
    precio: Optional[float] = Field(None, ge=0, description="Vehicle price")
    kilometraje: Optional[str] = Field(None, max_length=50, description="Vehicle mileage")
    estatus: VehicleStatus = Field(VehicleStatus.DISPONIBLE, description="Vehicle status")
    ubicacion: Optional[str] = Field(None, max_length=100, description="Vehicle location")
    descripcion: Optional[str] = Field(None, description="Vehicle description")
    caracteristicas: Optional[Dict[str, Any]] = Field(None, description="Additional vehicle characteristics")
    
    @validator('año')
    def validate_year(cls, v):
        """Validate vehicle year"""
        if v < 1900 or v > 2030:
            raise ValueError('Year must be between 1900 and 2030')
        return v
    
    @validator('precio')
    def validate_price(cls, v):
        """Validate vehicle price"""
        if v is not None and v < 0:
            raise ValueError('Price cannot be negative')
        return v
    
    @validator('marca', 'modelo')
    def validate_strings(cls, v):
        """Validate string fields"""
        if v and not v.strip():
            raise ValueError('String cannot be empty or whitespace only')
        return v.strip() if v else v

class VehicleCreate(VehicleBase):
    """Schema for creating a new vehicle"""
    
    created_by: Optional[str] = Field(None, max_length=100, description="User who created the vehicle")
    
    class Config:
        json_schema_extra = {
            "example": {
                "external_id": "V001",
                "marca": "Toyota",
                "modelo": "Camry",
                "año": 2020,
                "color": "Blanco",
                "precio": 25000.00,
                "kilometraje": "45,000 km",
                "estatus": "DISPONIBLE",
                "ubicacion": "Ciudad de México",
                "descripcion": "Excelente estado, un solo dueño",
                "caracteristicas": {
                    "grupo": "Sedán",
                    "transmision": "Automática",
                    "combustible": "Gasolina"
                },
                "created_by": "admin"
            }
        }

class VehicleUpdate(BaseModel):
    """Schema for updating an existing vehicle"""
    
    external_id: Optional[str] = Field(None, max_length=100)
    marca: Optional[str] = Field(None, max_length=100)
    modelo: Optional[str] = Field(None, max_length=100)
    año: Optional[int] = Field(None, ge=1900, le=2030)
    color: Optional[str] = Field(None, max_length=50)
    precio: Optional[float] = Field(None, ge=0)
    kilometraje: Optional[str] = Field(None, max_length=50)
    estatus: Optional[VehicleStatus] = None
    ubicacion: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    caracteristicas: Optional[Dict[str, Any]] = None
    
    @validator('año')
    def validate_year(cls, v):
        if v is not None and (v < 1900 or v > 2030):
            raise ValueError('Year must be between 1900 and 2030')
        return v
    
    @validator('precio')
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError('Price cannot be negative')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "precio": 24000.00,
                "estatus": "Apartado",
                "descripcion": "Vehiculo apartado - pendiente de pago"
            }
        }

class VehicleResponse(VehicleBase):
    """Schema for vehicle API responses"""
    
    id: int = Field(..., description="Vehicle ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    created_by: Optional[str] = Field(None, description="User who created the vehicle")
    updated_by: Optional[str] = Field(None, description="User who last updated the vehicle")
    photo_count: int = Field(0, description="Number of photos for this vehicle")
    is_available: bool = Field(..., description="Whether vehicle is available for sale")
    is_sold: bool = Field(..., description="Whether vehicle is sold")
    is_reserved: bool = Field(..., description="Whether vehicle is reserved")
    is_temporarily_unavailable: bool = Field(..., description="Whether vehicle is temporarily unavailable")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "external_id": "V001",
                "marca": "Toyota",
                "modelo": "Camry",
                "año": 2020,
                "color": "Blanco",
                "precio": 25000.00,
                "kilometraje": "45,000 km",
                "estatus": "Disponible",
                "ubicacion": "Ciudad de México",
                "descripcion": "Excelente estado, un solo dueño",
                "caracteristicas": {
                    "grupo": "Sedán",
                    "transmision": "Automática",
                    "combustible": "Gasolina"
                },
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-01T10:00:00Z",
                "created_by": "admin",
                "updated_by": "admin",
                "photo_count": 5,
                "is_available": True,
                "is_sold": False,
                "is_reserved": False,
                "is_temporarily_unavailable": False
            }
        }

class VehicleListResponse(BaseModel):
    """Schema for vehicle list API responses"""
    
    vehicles: List[VehicleResponse] = Field(..., description="List of vehicles")
    total: int = Field(..., description="Total number of vehicles")
    skip: int = Field(..., description="Number of records skipped")
    limit: int = Field(..., description="Number of records returned")
    
    class Config:
        json_schema_extra = {
            "example": {
                "vehicles": [],
                "total": 0,
                "skip": 0,
                "limit": 100
            }
        }

class VehicleStatusUpdate(BaseModel):
    """Schema for updating vehicle status"""
    
    estatus: VehicleStatus = Field(..., description="New vehicle status")
    changed_by: Optional[str] = Field(None, max_length=100, description="User who changed the status")
    reason: Optional[str] = Field(None, description="Reason for status change")
    notes: Optional[str] = Field(None, description="Additional notes about status change")
    
    class Config:
        json_schema_extra = {
            "example": {
                "estatus": "Apartado",
                "changed_by": "admin",
                "reason": "Cliente interesado",
                "notes": "Pendiente de pago inicial"
            }
        }

class VehicleSummary(BaseModel):
    """Schema for vehicle summary information"""
    
    id: int
    marca: str
    modelo: str
    año: int
    color: Optional[str]
    precio: Optional[float]
    estatus: VehicleStatus
    ubicacion: Optional[str]
    photo_count: int
    is_available: bool
    
    class Config:
        from_attributes = True

class VehicleStats(BaseModel):
    """Schema for vehicle statistics"""
    
    total_vehicles: int
    available_vehicles: int
    sold_vehicles: int
    reserved_vehicles: int
    temporarily_unavailable_vehicles: int
    average_price: Optional[float]
    total_value: Optional[float]
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_vehicles": 25,
                "available_vehicles": 18,
                "sold_vehicles": 5,
                "reserved_vehicles": 2,
                "temporarily_unavailable_vehicles": 0,
                "average_price": 32000.00,
                "total_value": 800000.00
            }
        }
