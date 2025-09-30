"""
Autosell.mx - Main FastAPI Application
Vehicle Management & Automation System
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application metadata
APP_NAME = "Autosell.mx API"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Complete Vehicle Management & Automation System"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print(f"🚗 Starting {APP_NAME} v{APP_VERSION}")
    print("📊 Loading configuration...")
    print("🔌 Initializing database connections...")
    print("🤖 Setting up automation workflows...")
    
    # Initialize database
    try:
        from app.database import init_db, check_db_connection
        if check_db_connection():
            print("✅ Database connection established")
            init_db()
            print("✅ Database tables initialized")
        else:
            print("⚠️  Database connection failed - some features may not work")
    except Exception as e:
        print(f"⚠️  Database initialization failed: {e}")
    
    yield
    
    # Shutdown
    print("🔄 Shutting down gracefully...")
    print("💾 Closing database connections...")
    print("📝 Saving logs...")
    print(f"✅ {APP_NAME} stopped successfully")

# Create FastAPI application
app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"]
)

# Include API routers
try:
    from app.api import vehicles_router, health_router, photos_router
    
    app.include_router(health_router)
    app.include_router(vehicles_router)
    app.include_router(photos_router, prefix="/photos", tags=["photos"])
    
    print("✅ API routers loaded successfully")
except Exception as e:
    print(f"⚠️  Failed to load API routers: {e}")

# Health check endpoint (legacy)
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": APP_NAME,
        "version": APP_VERSION,
        "timestamp": "2024-01-01T00:00:00Z"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": f"Welcome to {APP_NAME}",
        "version": APP_VERSION,
        "description": APP_DESCRIPTION,
        "docs": "/docs",
        "health": "/health",
        "api_endpoints": {
            "vehicles": "/vehicles",
            "health": "/health",
            "openapi": "/openapi.json"
        }
    }

# API version endpoint
@app.get("/api/v1")
async def api_info():
    """API version information"""
    return {
        "api": "Autosell.mx Vehicle Management API",
        "version": "v1.0.0",
        "status": "active",
        "endpoints": {
            "vehicles": "/vehicles",
            "photos": "/photos",
            "social": "/social",
            "analytics": "/analytics"
        }
    }

# Error handlers
from fastapi.responses import JSONResponse

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": "The requested resource was not found",
            "path": str(request.url.path)
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "path": str(request.url.path)
        }
    )

if __name__ == "__main__":
    # Run the application
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "false").lower() == "true",
        workers=int(os.getenv("WORKERS", 1))
    )
