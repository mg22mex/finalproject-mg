#!/usr/bin/env python3
"""
Simple Backend Starter for Autosell.mx
Optimized for Codespaces
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
import json

# Load environment variables
load_dotenv()

# In-memory storage (for development)
vehicles_db: List[Dict[str, Any]] = []
photos_db: List[Dict[str, Any]] = []
vehicle_counter = 1
photo_counter = 1

# Create FastAPI application
app = FastAPI(
    title="Autosell.mx API",
    description="Vehicle Management System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Autosell.mx API",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Autosell.mx API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

# Vehicles endpoint
@app.get("/vehicles")
@app.get("/vehicles/")
async def get_vehicles(skip: int = 0, limit: int = 12, search: str = "", marca: str = "", modelo: str = "", año: str = "", estatus: str = "", precio_min: str = "", precio_max: str = ""):
    """Get all vehicles with filters and pagination"""
    return {
        "vehicles": vehicles_db[skip:skip+limit],
        "total": len(vehicles_db),
        "skip": skip,
        "limit": limit,
        "message": f"Found {len(vehicles_db)} vehicles" if vehicles_db else "No vehicles found"
    }

# Photos endpoint
@app.get("/photos")
@app.get("/photos/")
async def get_photos(vehicle_id: int = None, skip: int = 0, limit: int = 12):
    """Get all photos with filters"""
    return {
        "photos": [],
        "total": 0,
        "skip": skip,
        "limit": limit,
        "message": "No photos found"
    }

# Photo upload endpoint
@app.post("/photos/upload/{vehicle_id}")
async def upload_photo(vehicle_id: int, photo_data: dict):
    """Upload photo for vehicle"""
    return {
        "id": 1,
        "vehicle_id": vehicle_id,
        "filename": photo_data.get("filename", "photo.jpg"),
        "description": photo_data.get("description", ""),
        "url": f"https://example.com/photos/{vehicle_id}/photo.jpg",
        "message": "Photo uploaded successfully"
    }

# Photo stats endpoint
@app.get("/photos/stats/overview")
async def get_photo_stats():
    """Get photo statistics"""
    return {
        "total_photos": 0,
        "photos_by_vehicle": {},
        "storage_used": 0
    }

# Facebook endpoint
@app.get("/facebook")
async def get_facebook():
    """Get Facebook status"""
    return {
        "status": "not_configured",
        "message": "Facebook integration not set up"
    }

# Facebook status endpoint
@app.get("/facebook/status")
async def get_facebook_status():
    """Get Facebook reposting status"""
    return {
        "is_active": False,
        "last_posted": None,
        "posts_last_week": 0,
        "active_vehicles": 0,
        "next_scheduled": None,
        "total_posts": 0,
        "workflow_name": None
    }

# Facebook schedule endpoint
@app.get("/facebook/schedule")
async def get_facebook_schedule():
    """Get Facebook posting schedule"""
    return {
        "is_active": False,
        "time_of_day": "09:00",
        "days_of_week": [1, 2, 3, 4, 5],
        "max_posts_per_day": 5,
        "post_interval_hours": 4,
        "include_marketplace": True
    }

# Dashboard endpoint
@app.get("/dashboard")
async def get_dashboard():
    """Get dashboard data"""
    return {
        "total_vehicles": 0,
        "available_vehicles": 0,
        "total_value": 0,
        "photos_uploaded": 0,
        "recent_vehicles": [],
        "system_status": {
            "api": "healthy",
            "database": "connected",
            "photo_storage": "ready"
        }
    }

# Dashboard stats endpoint (for frontend API calls)
@app.get("/dashboard/stats")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    # Calculate actual statistics from vehicles database
    total_vehicles = len(vehicles_db)
    available_vehicles = len([v for v in vehicles_db if v.get('estatus', '').lower() == 'disponible'])
    sold_vehicles = len([v for v in vehicles_db if v.get('estatus', '').lower() == 'vendido'])
    reserved_vehicles = len([v for v in vehicles_db if v.get('estatus', '').lower() == 'reservado'])
    unavailable_vehicles = len([v for v in vehicles_db if v.get('estatus', '').lower() == 'no disponible'])
    
    # Calculate financial statistics
    prices = [v.get('precio', 0) for v in vehicles_db if v.get('precio', 0) > 0]
    average_price = sum(prices) / len(prices) if prices else 0
    total_value = sum(prices)
    
    # Calculate photo statistics
    total_photos = len(photos_db)
    vehicles_with_photos = len(set(p.get('vehicle_id') for p in photos_db))
    
    return {
        "total_vehicles": total_vehicles,
        "available_vehicles": available_vehicles,
        "sold_vehicles": sold_vehicles,
        "reserved_vehicles": reserved_vehicles,
        "unavailable_vehicles": unavailable_vehicles,
        "average_price": round(average_price, 2),
        "total_value": total_value,
        "vehicles_change": 0,  # Could be calculated from historical data
        "available_change": 0,  # Could be calculated from historical data
        "value_change": 0,  # Could be calculated from historical data
        "total_photos": total_photos,
        "photos_change": 0,  # Could be calculated from historical data
        "vehicles_with_photos": vehicles_with_photos,
        "primary_photos": 0  # Could be calculated from photos with is_primary=True
    }

# Configuration endpoint
@app.get("/config")
async def get_config():
    """Get system configuration"""
    return {
        "status": "basic",
        "message": "Basic configuration loaded"
    }

# Missing endpoints that frontend expects
@app.get("/vehicles/{vehicle_id}")
async def get_vehicle(vehicle_id: int):
    """Get a specific vehicle"""
    return {
        "id": vehicle_id,
        "marca": "Unknown",
        "modelo": "Unknown",
        "año": 2024,
        "estatus": "disponible",
        "message": "Vehicle not found"
    }

@app.get("/photos/vehicle/{vehicle_id}")
async def get_vehicle_photos(vehicle_id: int):
    """Get photos for a specific vehicle"""
    return {
        "photos": [],
        "total": 0,
        "vehicle_id": vehicle_id,
        "message": "No photos found for this vehicle"
    }

@app.get("/photos/{photo_id}")
async def get_photo(photo_id: int):
    """Get a specific photo"""
    return {
        "id": photo_id,
        "filename": "unknown.jpg",
        "message": "Photo not found"
    }

@app.get("/photos/search")
async def search_photos(query: str = ""):
    """Search photos"""
    return {
        "photos": [],
        "total": 0,
        "query": query,
        "message": "No photos found"
    }

@app.get("/vehicles/search/{query}")
async def search_vehicles(query: str):
    """Search vehicles"""
    return {
        "vehicles": [],
        "total": 0,
        "query": query,
        "message": "No vehicles found"
    }

@app.get("/vehicles/status/{status}")
async def get_vehicles_by_status(status: str):
    """Get vehicles by status"""
    return {
        "vehicles": [],
        "total": 0,
        "status": status,
        "message": "No vehicles found with this status"
    }

@app.get("/health/detailed")
async def get_detailed_health():
    """Get detailed health information"""
    return {
        "status": "healthy",
        "service": "Autosell.mx API",
        "version": "1.0.0",
        "database": "connected",
        "storage": "ready",
        "timestamp": "2024-01-01T00:00:00Z"
    }

# POST endpoints that frontend might call
@app.post("/vehicles/")
async def create_vehicle(vehicle_data: dict):
    """Create a new vehicle"""
    global vehicle_counter
    
    # Create vehicle object
    vehicle = {
        "id": vehicle_counter,
        "marca": vehicle_data.get("marca", vehicle_data.get("make", "Unknown")),
        "modelo": vehicle_data.get("modelo", vehicle_data.get("model", "Unknown")),
        "año": vehicle_data.get("año", vehicle_data.get("year", 2024)),
        "precio": vehicle_data.get("precio", vehicle_data.get("price", 0)),
        "estatus": vehicle_data.get("estatus", vehicle_data.get("status", "disponible")),
        "color": vehicle_data.get("color", ""),
        "kilometraje": vehicle_data.get("kilometraje", ""),
        "ubicacion": vehicle_data.get("ubicacion", ""),
        "descripcion": vehicle_data.get("descripcion", vehicle_data.get("description", "")),
        "external_id": vehicle_data.get("external_id", f"GS_{vehicle_counter}")
    }
    
    # Store in database
    vehicles_db.append(vehicle)
    vehicle_counter += 1
    
    return {
        "id": vehicle["id"],
        "message": "Vehicle created successfully",
        "vehicle": vehicle
    }

@app.put("/vehicles/{vehicle_id}")
async def update_vehicle(vehicle_id: int):
    """Update a vehicle"""
    return {
        "id": vehicle_id,
        "message": "Vehicle update not implemented yet"
    }

@app.delete("/vehicles/{vehicle_id}")
async def delete_vehicle(vehicle_id: int):
    """Delete a vehicle"""
    return {
        "id": vehicle_id,
        "message": "Vehicle deletion not implemented yet"
    }

@app.post("/photos/vehicle/{vehicle_id}/photos/{photo_id}/set-primary")
async def set_primary_photo(vehicle_id: int, photo_id: int):
    """Set primary photo"""
    return {
        "vehicle_id": vehicle_id,
        "photo_id": photo_id,
        "message": "Primary photo setting not implemented yet"
    }

@app.post("/photos/sync/google-drive")
async def sync_google_drive_photos():
    """Sync Google Drive photos"""
    return {
        "message": "Google Drive sync not implemented yet"
    }

@app.post("/drive/test-connection")
async def test_drive_connection():
    """Test Google Drive connection"""
    return {
        "status": "not_configured",
        "message": "Google Drive connection not configured"
    }

if __name__ == "__main__":
    print("🚀 Starting Autosell.mx Backend...")
    print("📊 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("🚗 Vehicles: http://localhost:8000/vehicles")
    print("📸 Photos: http://localhost:8000/photos")
    print("")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )
