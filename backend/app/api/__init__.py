"""
API Package - REST endpoints for the vehicle management system
"""

from .vehicles import router as vehicles_router
from .endpoints.photos import router as photos_router
from .health import router as health_router

__all__ = [
    "vehicles_router",
    "photos_router", 
    "health_router"
]
