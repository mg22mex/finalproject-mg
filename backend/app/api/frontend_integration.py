"""
Frontend Integration API endpoints
Handles frontend → Google Sheets → Facebook automation
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any
import requests
import logging

from ..database import get_db
from ..models.vehicle import Vehicle, VehicleStatus

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/frontend", tags=["frontend-integration"])

@router.post("/sync-to-sheets")
async def sync_vehicle_to_sheets(
    vehicle_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Sync a single vehicle from frontend to Google Sheets
    """
    try:
        # Trigger n8n Google Sheets sync workflow
        n8n_webhook_url = "http://127.0.0.1:5678/webhook/sync-single-vehicle"
        
        response = requests.post(
            n8n_webhook_url,
            json=vehicle_data,
            timeout=30
        )
        
        if response.status_code == 200:
            logger.info(f"Vehicle synced to Google Sheets: {vehicle_data.get('marca')} {vehicle_data.get('modelo')}")
            return {
                "message": "Vehicle synced to Google Sheets successfully",
                "status": "success"
            }
        else:
            logger.error(f"Failed to sync to Google Sheets: {response.status_code}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to sync to Google Sheets"
            )
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error syncing to Google Sheets: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Network error connecting to automation service"
        )
    except Exception as e:
        logger.error(f"Error syncing vehicle to Google Sheets: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error syncing vehicle: {str(e)}"
        )

@router.post("/post-to-facebook")
async def post_vehicle_to_facebook(
    vehicle_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Post a vehicle to Facebook from frontend
    """
    try:
        # Trigger n8n Facebook posting workflow
        n8n_webhook_url = "http://127.0.0.1:5678/webhook/facebook-post"
        
        # Prepare Facebook post data
        facebook_data = {
            "account_type": "auto",  # or "manual" based on your setup
            "vehicle_data": vehicle_data,
            "message": f"🚗 {vehicle_data.get('marca')} {vehicle_data.get('modelo')} {vehicle_data.get('año')} - ${vehicle_data.get('precio', 0):,}"
        }
        
        response = requests.post(
            n8n_webhook_url,
            json=facebook_data,
            timeout=30
        )
        
        if response.status_code == 200:
            logger.info(f"Vehicle posted to Facebook: {vehicle_data.get('marca')} {vehicle_data.get('modelo')}")
            return {
                "message": "Vehicle posted to Facebook successfully",
                "status": "success"
            }
        else:
            logger.error(f"Failed to post to Facebook: {response.status_code}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to post to Facebook"
            )
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error posting to Facebook: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Network error connecting to automation service"
        )
    except Exception as e:
        logger.error(f"Error posting vehicle to Facebook: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error posting vehicle: {str(e)}"
        )

@router.post("/complete-vehicle-processing")
async def complete_vehicle_processing(
    vehicle_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """
    Complete vehicle processing: Database → Google Sheets → Facebook
    """
    try:
        # Step 1: Save to database (this should already be done by the frontend)
        # Step 2: Sync to Google Sheets
        sheets_response = await sync_vehicle_to_sheets(vehicle_data, db)
        
        # Step 3: Post to Facebook
        facebook_response = await post_vehicle_to_facebook(vehicle_data, db)
        
        logger.info(f"Complete processing successful for: {vehicle_data.get('marca')} {vehicle_data.get('modelo')}")
        
        return {
            "message": "Vehicle processing completed successfully",
            "google_sheets": sheets_response,
            "facebook": facebook_response,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error in complete vehicle processing: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error in complete processing: {str(e)}"
        )

@router.post("/trigger-sheets-sync")
async def trigger_sheets_sync(
    spreadsheet_id: str = None,
    db: Session = Depends(get_db)
):
    """
    Trigger full Google Sheets sync from frontend
    """
    try:
        # Trigger n8n Google Sheets sync workflow
        n8n_webhook_url = "http://127.0.0.1:5678/webhook/sync-from-sheets"
        
        payload = {}
        if spreadsheet_id:
            payload["spreadsheet_id"] = spreadsheet_id
        
        response = requests.post(
            n8n_webhook_url,
            json=payload,
            timeout=60  # Longer timeout for full sync
        )
        
        if response.status_code == 200:
            logger.info("Full Google Sheets sync triggered successfully")
            return {
                "message": "Google Sheets sync triggered successfully",
                "status": "success"
            }
        else:
            logger.error(f"Failed to trigger sheets sync: {response.status_code}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to trigger Google Sheets sync"
            )
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error triggering sheets sync: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Network error connecting to automation service"
        )
    except Exception as e:
        logger.error(f"Error triggering sheets sync: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error triggering sync: {str(e)}"
        )
