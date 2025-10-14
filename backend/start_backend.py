#!/usr/bin/env python3
"""
Simple Backend Starter for Autosell.mx
Optimized for Codespaces
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
import json
from google_drive_service import get_drive_service
import os
import requests
from datetime import datetime, timedelta
import time

# Add Facebook configuration
try:
    from facebook_config import (
        FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, FACEBOOK_ACCOUNTS,
        FACEBOOK_BASE_URL, DEFAULT_POSTING_SCHEDULE, MARKETPLACE_SETTINGS
    )
    FACEBOOK_ENABLED = True
    print("✅ Facebook integration enabled")
except ImportError:
    FACEBOOK_ENABLED = False
    print("⚠️ Facebook integration disabled - no config found")

# Load environment variables
load_dotenv()

# In-memory storage (for development)
vehicles_db: List[Dict[str, Any]] = []
photos_db: List[Dict[str, Any]] = []
vehicle_counter = 1
photo_counter = 1

# Create some sample photos for testing
def create_sample_photos():
    global photos_db, photo_counter
    sample_photos = [
        {
            "id": 1,
            "vehicle_id": 1,
            "filename": "toyota_corolla_front.jpg",
            "drive_file_id": "drive_1",
            "drive_url": "https://drive.google.com/file/d/drive_1/view",
            "file_size": 1024000,
            "mime_type": "image/jpeg",
            "uploaded_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": 2,
            "vehicle_id": 1,
            "filename": "toyota_corolla_side.jpg",
            "drive_file_id": "drive_2",
            "drive_url": "https://drive.google.com/file/d/drive_2/view",
            "file_size": 1200000,
            "mime_type": "image/jpeg",
            "uploaded_at": "2024-01-01T00:00:00Z"
        },
        {
            "id": 3,
            "vehicle_id": 1,
            "filename": "toyota_corolla_interior.jpg",
            "drive_file_id": "drive_3",
            "drive_url": "https://drive.google.com/file/d/drive_3/view",
            "file_size": 980000,
            "mime_type": "image/jpeg",
            "uploaded_at": "2024-01-01T00:00:00Z"
        }
    ]
    photos_db.extend(sample_photos)
    photo_counter = len(sample_photos)

# Initialize sample data
# create_sample_photos()  # Disabled to avoid sample data

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
    global photos_db
    
    if vehicle_id:
        filtered_photos = [photo for photo in photos_db if photo.get("vehicle_id") == vehicle_id]
    else:
        filtered_photos = photos_db
    
    total_photos = len(filtered_photos)
    paginated_photos = filtered_photos[skip:skip + limit]
    
    return {
        "photos": paginated_photos,
        "total": total_photos,
        "skip": skip,
        "limit": limit,
        "message": f"Found {total_photos} photos"
    }

# Photo upload endpoint
@app.post("/photos/upload/{vehicle_id}")
async def upload_photo(vehicle_id: int, request: Request):
    """Upload photo for vehicle"""
    global photo_counter, photos_db
    
    try:
        # Parse multipart form data
        form = await request.form()
        files = form.getlist("files")  # Frontend sends multiple files
        
        if not files:
            return {"error": "No files provided"}
        
        uploaded_photos = []
        
        # Get vehicle info for folder naming
        vehicle = next((v for v in vehicles_db if v.get('id') == vehicle_id), None)
        vehicle_name = f"{vehicle.get('marca', 'Unknown')}_{vehicle.get('modelo', 'Unknown')}" if vehicle else f"Vehicle_{vehicle_id}"
        
        # Enable Google Drive integration with working credentials
        use_google_drive = True
        print(f"📁 Using Google Drive for photo storage")
        
        if use_google_drive:
            try:
                print(f"📁 Uploading photos to Google Drive for vehicle {vehicle_id}")
                # Prepare photos for Google Drive upload
                photos_for_drive = []
                for file in files:
                    content = await file.read()
                    photos_for_drive.append({
                        'filename': file.filename or f"photo_{photo_counter + 1}.jpg",
                        'content': content
                    })
                
                # Get Google Drive service with working credentials
                drive_service = get_drive_service()
                if not drive_service or not drive_service.service:
                    print("⚠️ Google Drive service not available, falling back to local storage")
                    use_google_drive = False
                else:
                    # Upload to Google Drive
                    drive_photos = drive_service.upload_vehicle_photos(vehicle_id, vehicle_name, photos_for_drive)
            except Exception as e:
                print(f"⚠️ Google Drive upload failed: {e}")
                use_google_drive = False
        
        if use_google_drive:
            # Create photo records with Google Drive info
            for i, file in enumerate(files):
                photo_counter += 1
                photo_id = photo_counter
                filename = file.filename or f"photo_{photo_id}.jpg"
                
                # Use Google Drive info if available, otherwise use placeholder
                drive_photo = drive_photos[i] if i < len(drive_photos) else None
                
                photo = {
                    "id": photo_id,
                    "vehicle_id": vehicle_id,
                    "filename": filename,
                    "drive_file_id": drive_photo['drive_file_id'] if drive_photo else f"drive_{photo_id}",
                    "drive_url": drive_photo['drive_url'] if drive_photo else f"https://drive.google.com/file/d/drive_{photo_id}/view",
                    "file_size": len(await file.read()) if hasattr(file, 'read') else 0,
                    "mime_type": file.content_type or "image/jpeg",
                    "uploaded_at": "2024-01-01T00:00:00Z"
                }
                
                photos_db.append(photo)
                uploaded_photos.append(photo)
        else:
            print(f"📁 Google Drive not available, using local storage for vehicle {vehicle_id}")
            # Fallback to local storage
            for file in files:
                photo_counter += 1
                photo_id = photo_counter
                
                # Get file info
                filename = file.filename or f"photo_{photo_id}.jpg"
                content = await file.read()
                file_size = len(content)
                
                # Save the actual image file
                import os
                uploads_dir = "uploads"
                os.makedirs(uploads_dir, exist_ok=True)
                file_path = os.path.join(uploads_dir, f"photo_{photo_id}_{filename}")
                
                with open(file_path, "wb") as f:
                    f.write(content)
                
                # Create photo record
                photo = {
                    "id": photo_id,
                    "vehicle_id": vehicle_id,
                    "filename": filename,
                    "drive_file_id": f"local_{photo_id}",
                    "drive_url": f"http://localhost:8000/photos/image/{photo_id}",
                    "file_path": file_path,  # Store the actual file path
                    "file_size": file_size,
                    "mime_type": file.content_type or "image/jpeg",
                    "uploaded_at": "2024-01-01T00:00:00Z"
                }
                
                photos_db.append(photo)
                uploaded_photos.append(photo)
        
        return {
            "photos": uploaded_photos,
            "total": len(uploaded_photos),
            "vehicle_id": vehicle_id,
            "message": f"Successfully uploaded {len(uploaded_photos)} photos",
            "google_drive_used": use_google_drive
        }
    except Exception as e:
        return {"error": f"Upload failed: {str(e)}"}

# Serve photo images
@app.get("/photos/image/{photo_id}")
async def serve_photo(photo_id: int):
    """Serve photo image"""
    global photos_db
    
    # Find the photo
    photo = next((p for p in photos_db if p.get("id") == photo_id), None)
    if not photo:
        return {"error": "Photo not found"}
    
    # Check if it's a Google Drive photo
    drive_file_id = photo.get('drive_file_id', '')
    if drive_file_id and not drive_file_id.startswith('local_'):
        # This is a Google Drive photo, download and serve it
        try:
            from google_drive_service import get_drive_service
            drive_service = get_drive_service()
            if drive_service and drive_service.service:
                # Download the image from Google Drive
                request = drive_service.service.files().get_media(fileId=drive_file_id)
                image_data = request.execute()
                
                # Return the image data with proper headers
                from fastapi.responses import Response
                mime_type = photo.get('mime_type', 'image/jpeg')
                return Response(content=image_data, media_type=mime_type)
            else:
                # Fallback to SVG placeholder if service not available
                filename = photo.get('filename', 'Image')
                svg_content = f"""
                <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
                    <rect width="300" height="200" fill="#f3f4f6"/>
                    <text x="150" y="100" text-anchor="middle" fill="#9ca3af" font-family="Arial, sans-serif" font-size="14">
                        Drive service not available
                    </text>
                </svg>
                """
                from fastapi.responses import Response
                return Response(content=svg_content, media_type="image/svg+xml")
        except Exception as e:
            print(f"Error serving Google Drive photo: {e}")
            # Fallback to SVG placeholder
            filename = photo.get('filename', 'Image')
            svg_content = f"""
            <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
                <rect width="300" height="200" fill="#f3f4f6"/>
                <text x="150" y="100" text-anchor="middle" fill="#9ca3af" font-family="Arial, sans-serif" font-size="14">
                    Error loading image
                </text>
            </svg>
            """
            from fastapi.responses import Response
            return Response(content=svg_content, media_type="image/svg+xml")
    
    # Serve local photo file
    file_path = photo.get('file_path')
    if file_path and os.path.exists(file_path):
        from fastapi.responses import FileResponse
        mime_type = photo.get('mime_type', 'image/jpeg')
        return FileResponse(file_path, media_type=mime_type)
    
    # Fallback to SVG placeholder if file doesn't exist
    filename = photo.get('filename', 'Image')
    svg_content = f"""
    <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="200" fill="#4f46e5"/>
        <text x="150" y="100" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="14">
            {filename}
        </text>
        <text x="150" y="120" text-anchor="middle" fill="white" font-family="Arial, sans-serif" font-size="12">
            Photo ID: {photo_id}
        </text>
    </svg>
    """
    
    from fastapi.responses import Response
    return Response(content=svg_content, media_type="image/svg+xml")

# Primary photo endpoint for vehicles
@app.get("/vehicles/{vehicle_id}/primary-photo")
async def get_vehicle_primary_photo(vehicle_id: int):
    """Get primary photo for a vehicle"""
    global photos_db
    
    # Find the primary photo for this vehicle
    primary_photo = next((p for p in photos_db if p.get("vehicle_id") == vehicle_id and p.get("is_primary", False)), None)
    
    if not primary_photo:
        # If no primary photo, get the first photo for this vehicle
        primary_photo = next((p for p in photos_db if p.get("vehicle_id") == vehicle_id), None)
    
    if not primary_photo:
        # Return placeholder if no photos
        from fastapi.responses import Response
        svg_content = f"""
        <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
            <rect width="300" height="200" fill="#f3f4f6"/>
            <text x="150" y="100" text-anchor="middle" fill="#9ca3af" font-family="Arial, sans-serif" font-size="14">
                No photos available
            </text>
        </svg>
        """
        return Response(content=svg_content, media_type="image/svg+xml")
    
    # Redirect to the photo image endpoint
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"/photos/image/{primary_photo['id']}")

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
    prices = [v.get('precio', 0) for v in vehicles_db if v.get('precio', 0) is not None and v.get('precio', 0) > 0]
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
    global vehicles_db
    
    # Find the vehicle in the database
    vehicle = next((v for v in vehicles_db if v.get("id") == vehicle_id), None)
    
    if not vehicle:
        return {
            "id": vehicle_id,
            "marca": "Unknown",
            "modelo": "Unknown",
            "año": 2024,
            "estatus": "disponible",
            "message": "Vehicle not found"
        }
    
    return vehicle

@app.get("/photos/vehicle/{vehicle_id}")
async def get_vehicle_photos(vehicle_id: int):
    """Get photos for a specific vehicle"""
    global photos_db
    
    vehicle_photos = [photo for photo in photos_db if photo.get("vehicle_id") == vehicle_id]
    
    return {
        "photos": vehicle_photos,
        "total": len(vehicle_photos),
        "vehicle_id": vehicle_id,
        "message": f"Found {len(vehicle_photos)} photos for this vehicle"
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
    # Filter vehicles based on search query
    filtered_vehicles = []
    query_lower = query.lower()
    
    for vehicle in vehicles_db:
        # Search in marca, modelo, año, color, descripcion
        if (query_lower in str(vehicle.get('marca', '')).lower() or
            query_lower in str(vehicle.get('modelo', '')).lower() or
            query_lower in str(vehicle.get('año', '')).lower() or
            query_lower in str(vehicle.get('color', '')).lower() or
            query_lower in str(vehicle.get('descripcion', '')).lower()):
            filtered_vehicles.append(vehicle)
    
    return {
        "vehicles": filtered_vehicles,
        "total": len(filtered_vehicles),
        "query": query,
        "message": f"Found {len(filtered_vehicles)} vehicles matching '{query}'"
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
async def create_vehicle(request: Request):
    """Create a new vehicle or multiple vehicles"""
    global vehicle_counter
    
    # Get the request body
    vehicle_data = await request.json()
    
    # Handle both single vehicle and array of vehicles
    if isinstance(vehicle_data, list):
        # Multiple vehicles from N8N
        created_vehicles = []
        for data in vehicle_data:
            vehicle = {
                "id": vehicle_counter,
                "marca": data.get("marca", data.get("make", "Unknown")),
                "modelo": data.get("modelo", data.get("model", "Unknown")),
                "año": data.get("año", data.get("year", 2024)),
                "precio": data.get("precio", data.get("price", 0)),
                "estatus": data.get("estatus", data.get("status", "disponible")),
                "color": data.get("color", ""),
                "kilometraje": data.get("kilometraje", ""),
                "ubicacion": data.get("ubicacion", ""),
                "descripcion": data.get("descripcion", data.get("description", "")),
                "external_id": data.get("external_id", f"GS_{vehicle_counter}")
            }
            
            # Store in database
            vehicles_db.append(vehicle)
            created_vehicles.append(vehicle)
            vehicle_counter += 1
        
        return {
            "vehicles": created_vehicles,
            "total": len(created_vehicles),
            "message": f"Successfully created {len(created_vehicles)} vehicles"
        }
    else:
        # Single vehicle
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

@app.delete("/vehicles/clear")
async def clear_all_vehicles():
    """Clear all vehicles from database"""
    try:
        # Clear all vehicles from the database
        vehicles_db.clear()
        return {
            "message": "All vehicles cleared successfully",
            "count": 0
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "Failed to clear vehicles"
        }

@app.put("/vehicles/{vehicle_id}")
async def update_vehicle(vehicle_id: int, vehicle_data: dict):
    """Update a vehicle"""
    global vehicles_db
    
    try:
        print(f"🔄 Updating vehicle {vehicle_id}")
        print(f"📊 Current vehicles count: {len(vehicles_db)}")
        
        # Find the vehicle
        vehicle_index = None
        for i, vehicle in enumerate(vehicles_db):
            if vehicle.get('id') == vehicle_id:
                vehicle_index = i
                break
        
        if vehicle_index is None:
            print(f"❌ Vehicle {vehicle_id} not found in database")
            return {
                "error": "Vehicle not found",
                "id": vehicle_id
            }
        
        # Update the vehicle with new data
        updated_vehicle = vehicles_db[vehicle_index].copy()
        updated_vehicle.update(vehicle_data)
        updated_vehicle['id'] = vehicle_id  # Ensure ID doesn't change
        
        # Update the vehicle in the database
        vehicles_db[vehicle_index] = updated_vehicle
        
        print(f"✅ Vehicle {vehicle_id} updated successfully")
        print(f"📊 Final vehicles count: {len(vehicles_db)}")
        
        return {
            "id": vehicle_id,
            "message": "Vehicle updated successfully",
            "updated_vehicle": updated_vehicle
        }
    except Exception as e:
        print(f"❌ Error updating vehicle {vehicle_id}: {e}")
        return {
            "error": str(e),
            "message": "Failed to update vehicle"
        }

@app.delete("/vehicles/{vehicle_id}")
async def delete_vehicle(vehicle_id: int):
    """Delete a vehicle"""
    global vehicles_db, photos_db
    
    try:
        print(f"🗑️ Attempting to delete vehicle {vehicle_id}")
        print(f"📊 Current vehicles count: {len(vehicles_db)}")
        print(f"📸 Current photos count: {len(photos_db)}")
        
        # Find and remove the vehicle
        vehicle_index = None
        for i, vehicle in enumerate(vehicles_db):
            if vehicle.get('id') == vehicle_id:
                vehicle_index = i
                break
        
        if vehicle_index is None:
            print(f"❌ Vehicle {vehicle_id} not found in database")
            return {
                "error": "Vehicle not found",
                "id": vehicle_id
            }
        
        # Remove the vehicle
        deleted_vehicle = vehicles_db.pop(vehicle_index)
        print(f"✅ Vehicle {vehicle_id} deleted from database")
        
        # Remove associated photos
        photos_before = len(photos_db)
        photos_db = [photo for photo in photos_db if photo.get('vehicle_id') != vehicle_id]
        photos_removed = photos_before - len(photos_db)
        print(f"📸 Removed {photos_removed} photos for vehicle {vehicle_id}")
        
        print(f"📊 Final vehicles count: {len(vehicles_db)}")
        print(f"📸 Final photos count: {len(photos_db)}")
        
        return {
            "id": vehicle_id,
            "message": "Vehicle deleted successfully",
            "deleted_vehicle": deleted_vehicle,
            "photos_removed": photos_removed
        }
    except Exception as e:
        print(f"❌ Error deleting vehicle {vehicle_id}: {e}")
        return {
            "error": str(e),
            "message": "Failed to delete vehicle"
        }

@app.put("/photos/{photo_id}/set-primary")
async def set_primary_photo(photo_id: int):
    """Set a photo as primary for its vehicle"""
    global photos_db
    
    try:
        print(f"⭐ Setting photo {photo_id} as primary")
        
        # Find the photo
        photo = next((p for p in photos_db if p.get('id') == photo_id), None)
        if not photo:
            return {
                "error": "Photo not found",
                "id": photo_id
            }
        
        vehicle_id = photo.get('vehicle_id')
        if not vehicle_id:
            return {
                "error": "Photo has no associated vehicle",
                "id": photo_id
            }
        
        # Remove primary status from all other photos of this vehicle
        for p in photos_db:
            if p.get('vehicle_id') == vehicle_id:
                p['is_primary'] = False
        
        # Set this photo as primary
        photo['is_primary'] = True
        
        print(f"✅ Photo {photo_id} set as primary for vehicle {vehicle_id}")
        
        return {
            "id": photo_id,
            "message": "Photo set as primary successfully",
            "vehicle_id": vehicle_id
        }
    except Exception as e:
        print(f"❌ Error setting primary photo: {e}")
        return {
            "error": str(e),
            "message": "Failed to set primary photo"
        }

@app.delete("/photos/{photo_id}")
async def delete_photo(photo_id: int):
    """Delete a photo"""
    global photos_db
    
    try:
        # Find and remove the photo
        photo_index = None
        for i, photo in enumerate(photos_db):
            if photo.get('id') == photo_id:
                photo_index = i
                break
        
        if photo_index is None:
            return {
                "error": "Photo not found",
                "id": photo_id
            }
        
        # Remove the photo
        deleted_photo = photos_db.pop(photo_index)
        
        return {
            "id": photo_id,
            "message": "Photo deleted successfully",
            "deleted_photo": deleted_photo
        }
    except Exception as e:
        return {
            "error": str(e),
            "message": "Failed to delete photo"
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

# Facebook endpoints
@app.get("/facebook/accounts")
async def get_facebook_accounts():
    """Get all Facebook accounts"""
    if not FACEBOOK_ENABLED:
        return {"error": "Facebook integration not enabled"}
    
    return {
        "accounts": FACEBOOK_ACCOUNTS,
        "total": len(FACEBOOK_ACCOUNTS)
    }

@app.post("/facebook/accounts/{account_id}/test")
async def test_facebook_account(account_id: int):
    """Test Facebook account connection"""
    if not FACEBOOK_ENABLED:
        return {"error": "Facebook integration not enabled"}
    
    if account_id >= len(FACEBOOK_ACCOUNTS):
        return {"error": "Account not found"}
    
    account = FACEBOOK_ACCOUNTS[account_id]
    
    try:
        # Test the access token
        response = requests.get(
            f"{FACEBOOK_BASE_URL}/me",
            params={"access_token": account["access_token"]}
        )
        
        if response.status_code == 200:
            user_data = response.json()
            return {
                "success": True,
                "account_name": account["account_name"],
                "user_id": user_data.get("id"),
                "user_name": user_data.get("name"),
                "message": "Connection successful"
            }
        else:
            return {
                "success": False,
                "error": f"Facebook API error: {response.status_code}",
                "details": response.text
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/facebook/vehicles/{vehicle_id}/post")
async def post_vehicle_to_facebook(vehicle_id: int, account_id: int = 0):
    """Post a vehicle to Facebook"""
    if not FACEBOOK_ENABLED:
        return {"error": "Facebook integration not enabled"}
    
    if account_id >= len(FACEBOOK_ACCOUNTS):
        return {"error": "Account not found"}
    
    # Find the vehicle
    vehicle = next((v for v in vehicles_db if v.get('id') == vehicle_id), None)
    if not vehicle:
        return {"error": "Vehicle not found"}
    
    account = FACEBOOK_ACCOUNTS[account_id]
    
    try:
        # Get primary photo
        primary_photo = next((p for p in photos_db if p.get('vehicle_id') == vehicle_id and p.get('is_primary')), None)
        
        # Create post content
        post_content = f"""
🚗 {vehicle['marca']} {vehicle['modelo']} {vehicle['año']}

💰 Precio: ${vehicle['precio']:,}
 Color: {vehicle['color']}
 Kilómetros: {vehicle['kilometraje']:,}
 Estado: {vehicle['estatus']}

📞 Contacto: Autosell.mx
 Más información: https://autosell.mx/vehiculo/{vehicle_id}
        """.strip()
        
        # Post to Facebook (simplified - just to page for now)
        if account["page_id"]:
            # Post to page
            response = requests.post(
                f"{FACEBOOK_BASE_URL}/{account['page_id']}/feed",
                data={
                    "message": post_content,
                    "access_token": account["access_token"]
                }
            )
        else:
            # Post to user timeline (simplified)
            response = requests.post(
                f"{FACEBOOK_BASE_URL}/me/feed",
                data={
                    "message": post_content,
                    "access_token": account["access_token"]
                }
            )
        
        if response.status_code == 200:
            post_data = response.json()
            return {
                "success": True,
                "post_id": post_data.get("id"),
                "message": "Vehicle posted successfully to Facebook"
            }
        else:
            return {
                "success": False,
                "error": f"Facebook API error: {response.status_code}",
                "details": response.text
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.delete("/facebook/vehicles/{vehicle_id}/remove")
async def remove_vehicle_from_facebook(vehicle_id: int, account_id: int = 0):
    """Remove a vehicle from Facebook (when marked as vendido)"""
    if not FACEBOOK_ENABLED:
        return {"error": "Facebook integration not enabled"}
    
    # This would require storing post IDs when posting
    # For now, return a placeholder
    return {
        "success": True,
        "message": "Vehicle removal from Facebook (placeholder - requires post ID tracking)"
    }

@app.get("/facebook/automation/status")
async def get_automation_status():
    """Get Facebook automation status"""
    if not FACEBOOK_ENABLED:
        return {"error": "Facebook integration not enabled"}
    
    return {
        "enabled": MARKETPLACE_SETTINGS["enabled"],
        "auto_repost": MARKETPLACE_SETTINGS["auto_repost"],
        "remove_sold": MARKETPLACE_SETTINGS["remove_sold"],
        "posting_schedule": DEFAULT_POSTING_SCHEDULE,
        "accounts_configured": len(FACEBOOK_ACCOUNTS)
    }

if __name__ == "__main__":
    print("🚀 Starting Autosell.mx Backend...")
    print("📊 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8001/health")
    print("🚗 Vehicles: http://localhost:8001/vehicles")
    print("📸 Photos: http://localhost:8001/photos")
    print("")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        reload=False
    )
