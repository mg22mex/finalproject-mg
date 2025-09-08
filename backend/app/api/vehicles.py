"""
Vehicle API endpoints - CRUD operations for vehicles
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
import logging

from ..database import get_db
from ..models.vehicle import Vehicle, VehicleStatus
from ..schemas.vehicle import (
    VehicleCreate, 
    VehicleUpdate, 
    VehicleResponse, 
    VehicleListResponse,
    VehicleStatusUpdate
)

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/vehicles", tags=["vehicles"])

@router.get("/", response_model=VehicleListResponse)
async def get_vehicles(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    marca: Optional[str] = Query(None, description="Filter by brand"),
    modelo: Optional[str] = Query(None, description="Filter by model"),
    año: Optional[int] = Query(None, description="Filter by year"),
    estatus: Optional[VehicleStatus] = Query(None, description="Filter by status"),
    precio_min: Optional[float] = Query(None, ge=0, description="Minimum price"),
    precio_max: Optional[float] = Query(None, ge=0, description="Maximum price"),
    search: Optional[str] = Query(None, description="Search in marca, modelo, descripcion"),
    db: Session = Depends(get_db)
):
    """
    Get list of vehicles with optional filtering and pagination
    """
    try:
        # Build query
        query = db.query(Vehicle)
        
        # Apply filters
        if marca:
            query = query.filter(Vehicle.marca.ilike(f"%{marca}%"))
        
        if modelo:
            query = query.filter(Vehicle.modelo.ilike(f"%{modelo}%"))
        
        if año:
            query = query.filter(Vehicle.año == año)
        
        if estatus:
            query = query.filter(Vehicle.estatus == estatus)
        
        if precio_min is not None:
            query = query.filter(Vehicle.precio >= precio_min)
        
        if precio_max is not None:
            query = query.filter(Vehicle.precio <= precio_max)
        
        # Search functionality
        if search:
            search_filter = or_(
                Vehicle.marca.ilike(f"%{search}%"),
                Vehicle.modelo.ilike(f"%{search}%"),
                Vehicle.descripcion.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        vehicles = query.order_by(Vehicle.created_at.desc()).offset(skip).limit(limit).all()
        
        # Convert to response format
        vehicle_list = [VehicleResponse.from_orm(vehicle) for vehicle in vehicles]
        
        logger.info(f"Retrieved {len(vehicle_list)} vehicles (total: {total})")
        
        return VehicleListResponse(
            vehicles=vehicle_list,
            total=total,
            skip=skip,
            limit=limit
        )
        
    except Exception as e:
        logger.error(f"Error retrieving vehicles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving vehicles"
        )

@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific vehicle by ID
    """
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle with ID {vehicle_id} not found"
            )
        
        logger.info(f"Retrieved vehicle {vehicle_id}: {vehicle.display_name}")
        return VehicleResponse.from_orm(vehicle)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving vehicle {vehicle_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving vehicle"
        )

@router.post("/", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new vehicle
    """
    try:
        # Check if external_id already exists
        if vehicle_data.external_id:
            existing = db.query(Vehicle).filter(Vehicle.external_id == vehicle_data.external_id).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Vehicle with external ID {vehicle_data.external_id} already exists"
                )
        
        # Create vehicle
        vehicle = Vehicle(**vehicle_data.dict())
        db.add(vehicle)
        db.commit()
        db.refresh(vehicle)
        
        logger.info(f"Created vehicle {vehicle.id}: {vehicle.display_name}")
        return VehicleResponse.from_orm(vehicle)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating vehicle: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while creating vehicle"
        )

@router.put("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing vehicle
    """
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle with ID {vehicle_id} not found"
            )
        
        # Check external_id uniqueness if being updated
        if vehicle_data.external_id and vehicle_data.external_id != vehicle.external_id:
            existing = db.query(Vehicle).filter(
                and_(
                    Vehicle.external_id == vehicle_data.external_id,
                    Vehicle.id != vehicle_id
                )
            ).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Vehicle with external ID {vehicle_data.external_id} already exists"
                )
        
        # Update fields
        update_data = vehicle_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(vehicle, field, value)
        
        vehicle.updated_by = "api_user"  # TODO: Get from authentication
        db.commit()
        db.refresh(vehicle)
        
        logger.info(f"Updated vehicle {vehicle_id}: {vehicle.display_name}")
        return VehicleResponse.from_orm(vehicle)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating vehicle {vehicle_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while updating vehicle"
        )

@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a vehicle
    """
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle with ID {vehicle_id} not found"
            )
        
        # Check if vehicle can be deleted (not sold, etc.)
        if vehicle.estatus == VehicleStatus.VENDIDO:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete sold vehicles"
            )
        
        # Delete vehicle (cascade will handle related records)
        db.delete(vehicle)
        db.commit()
        
        logger.info(f"Deleted vehicle {vehicle_id}: {vehicle.display_name}")
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting vehicle {vehicle_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while deleting vehicle"
        )

@router.patch("/{vehicle_id}/status", response_model=VehicleResponse)
async def update_vehicle_status(
    vehicle_id: int,
    status_update: VehicleStatusUpdate,
    db: Session = Depends(get_db)
):
    """
    Update vehicle status
    """
    try:
        vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
        
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vehicle with ID {vehicle_id} not found"
            )
        
        # Update status and create history record
        status_record = vehicle.update_status(
            new_status=status_update.estatus,
            changed_by=status_update.changed_by or "api_user",
            reason=status_update.reason,
            notes=status_update.notes
        )
        
        # Add status history record
        db.add(status_record)
        db.commit()
        db.refresh(vehicle)
        
        logger.info(f"Updated status for vehicle {vehicle_id} to {status_update.estatus}")
        return VehicleResponse.from_orm(vehicle)
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating status for vehicle {vehicle_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while updating vehicle status"
        )

@router.get("/status/{estatus}", response_model=VehicleListResponse)
async def get_vehicles_by_status(
    estatus: VehicleStatus,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get vehicles by specific status
    """
    try:
        query = db.query(Vehicle).filter(Vehicle.estatus == estatus)
        total = query.count()
        
        vehicles = query.order_by(Vehicle.created_at.desc()).offset(skip).limit(limit).all()
        vehicle_list = [VehicleResponse.from_orm(vehicle) for vehicle in vehicles]
        
        logger.info(f"Retrieved {len(vehicle_list)} vehicles with status {estatus}")
        
        return VehicleListResponse(
            vehicles=vehicle_list,
            total=total,
            skip=skip,
            limit=limit
        )
        
    except Exception as e:
        logger.error(f"Error retrieving vehicles by status {estatus}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while retrieving vehicles by status"
        )

@router.get("/search/{query}", response_model=VehicleListResponse)
async def search_vehicles(
    query: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Search vehicles by text query
    """
    try:
        search_filter = or_(
            Vehicle.marca.ilike(f"%{query}%"),
            Vehicle.modelo.ilike(f"%{query}%"),
            Vehicle.descripcion.ilike(f"%{query}%"),
            Vehicle.color.ilike(f"%{query}%"),
            Vehicle.ubicacion.ilike(f"%{query}%")
        )
        
        db_query = db.query(Vehicle).filter(search_filter)
        total = db_query.count()
        
        vehicles = db_query.order_by(Vehicle.created_at.desc()).offset(skip).limit(limit).all()
        vehicle_list = [VehicleResponse.from_orm(vehicle) for vehicle in vehicles]
        
        logger.info(f"Search '{query}' returned {len(vehicle_list)} vehicles")
        
        return VehicleListResponse(
            vehicles=vehicle_list,
            total=total,
            skip=skip,
            limit=limit
        )
        
    except Exception as e:
        logger.error(f"Error searching vehicles with query '{query}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while searching vehicles"
        )
