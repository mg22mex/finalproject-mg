from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Dict, Any
from app.database import get_db
from app.models.vehicle import Vehicle
from app.models.photo import Photo

router = APIRouter(tags=["dashboard"])

@router.get("/stats")
async def get_dashboard_stats(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Get comprehensive dashboard statistics
    """
    try:
        # Get total vehicles count
        total_vehicles = db.query(Vehicle).count()
        
        # Get vehicles by status
        available_vehicles = db.query(Vehicle).filter(Vehicle.estatus == "DISPONIBLE").count()
        sold_vehicles = db.query(Vehicle).filter(Vehicle.estatus == "VENDIDO").count()
        reserved_vehicles = db.query(Vehicle).filter(Vehicle.estatus == "APARTADO").count()
        unavailable_vehicles = db.query(Vehicle).filter(Vehicle.estatus == "AUSENTE").count()
        
        # Calculate total value (only for available vehicles)
        total_value_result = db.query(func.sum(Vehicle.precio)).filter(
            and_(Vehicle.estatus == "DISPONIBLE", Vehicle.precio.isnot(None))
        ).scalar()
        total_value = float(total_value_result) if total_value_result else 0.0
        
        # Calculate average price (only for available vehicles with price)
        avg_price_result = db.query(func.avg(Vehicle.precio)).filter(
            and_(Vehicle.estatus == "DISPONIBLE", Vehicle.precio.isnot(None))
        ).scalar()
        average_price = float(avg_price_result) if avg_price_result else 0.0
        
        # Get total photos count
        total_photos = db.query(Photo).count()
        
        # Get vehicles with photos count
        vehicles_with_photos = db.query(Vehicle.id).join(Photo).distinct().count()
        
        # Get primary photos count
        primary_photos = db.query(Photo).filter(Photo.is_primary == True).count()
        
        # Calculate percentage changes (mock for now - in real app, compare with previous period)
        vehicles_change = 0.0  # Would calculate from previous period
        available_change = 0.0
        value_change = 0.0
        photos_change = 0.0
        
        return {
            "total_vehicles": total_vehicles,
            "available_vehicles": available_vehicles,
            "sold_vehicles": sold_vehicles,
            "reserved_vehicles": reserved_vehicles,
            "unavailable_vehicles": unavailable_vehicles,
            "total_value": total_value,
            "average_price": average_price,
            "total_photos": total_photos,
            "vehicles_with_photos": vehicles_with_photos,
            "primary_photos": primary_photos,
            "vehicles_change": vehicles_change,
            "available_change": available_change,
            "value_change": value_change,
            "photos_change": photos_change,
            "status_breakdown": {
                "disponible": available_vehicles,
                "vendido": sold_vehicles,
                "reservado": reserved_vehicles,
                "no_disponible": unavailable_vehicles
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating dashboard stats: {str(e)}"
        )

@router.get("/recent-vehicles")
async def get_recent_vehicles(limit: int = 6, db: Session = Depends(get_db)):
    """
    Get recent vehicles for dashboard display
    """
    try:
        vehicles = db.query(Vehicle).order_by(Vehicle.created_at.desc()).limit(limit).all()
        
        return {
            "vehicles": [
                {
                    "id": vehicle.id,
                    "marca": vehicle.marca or "Unknown",
                    "modelo": vehicle.modelo or "Unknown", 
                    "año": vehicle.año,
                    "precio": vehicle.precio,
                    "estatus": vehicle.estatus,
                    "color": vehicle.color,
                    "kilometraje": vehicle.kilometraje,
                    "ubicacion": vehicle.ubicacion,
                    "created_at": vehicle.created_at.isoformat() if vehicle.created_at else None
                }
                for vehicle in vehicles
            ]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching recent vehicles: {str(e)}"
        )
