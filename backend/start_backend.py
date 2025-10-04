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

# Load environment variables
load_dotenv()

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
        "vehicles": [],
        "total": 0,
        "skip": skip,
        "limit": limit,
        "message": "No vehicles found"
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
async def upload_photo(vehicle_id: int):
    """Upload photo for vehicle"""
    return {
        "message": "Photo upload not implemented yet",
        "vehicle_id": vehicle_id
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
    return {
        "total_vehicles": 0,
        "available_vehicles": 0,
        "sold_vehicles": 0,
        "reserved_vehicles": 0,
        "unavailable_vehicles": 0,
        "average_price": 0,
        "total_value": 0,
        "vehicles_change": 0,
        "available_change": 0,
        "value_change": 0,
        "total_photos": 0,
        "photos_change": 0,
        "vehicles_with_photos": 0,
        "primary_photos": 0
    }

# Configuration endpoint
@app.get("/config")
async def get_config():
    """Get system configuration"""
    return {
        "status": "basic",
        "message": "Basic configuration loaded"
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
