"""
Health Check API - System monitoring and status endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
import logging
import os
from datetime import datetime

from ..database import get_db, health_check as db_health_check

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def health_check() -> Dict[str, Any]:
    """
    Basic health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Autosell.mx API",
        "version": "1.0.0"
    }

@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Detailed health check including database status
    """
    try:
        # Database health check
        db_status = db_health_check()
        
        # System information
        system_info = {
            "python_version": os.sys.version,
            "environment": os.getenv("APP_ENV", "development"),
            "debug_mode": os.getenv("DEBUG", "false").lower() == "true"
        }
        
        # Overall health status
        overall_status = "healthy"
        if db_status["status"] != "healthy":
            overall_status = "degraded"
        
        health_data = {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "service": "Autosell.mx API",
            "version": "1.0.0",
            "database": db_status,
            "system": system_info
        }
        
        logger.info(f"Health check completed: {overall_status}")
        return health_data
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "Autosell.mx API",
            "version": "1.0.0",
            "error": str(e)
        }

@router.get("/ready")
async def readiness_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Readiness check for load balancers and orchestration systems
    """
    try:
        # Check database connection
        db_status = db_health_check()
        
        # Determine if service is ready
        is_ready = db_status["status"] in ["healthy", "degraded"]
        
        if is_ready:
            logger.info("Readiness check passed")
            return {
                "status": "ready",
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            logger.warning("Readiness check failed")
            return {
                "status": "not_ready",
                "timestamp": datetime.utcnow().isoformat(),
                "reason": "Database connection failed"
            }
            
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return {
            "status": "not_ready",
            "timestamp": datetime.utcnow().isoformat(),
            "reason": str(e)
        }

@router.get("/live")
async def liveness_check() -> Dict[str, Any]:
    """
    Liveness check for Kubernetes and container orchestration
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }
