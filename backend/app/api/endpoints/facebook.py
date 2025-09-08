"""
Facebook Reposting API Endpoints
Daily automation for vehicle listings on Facebook and Marketplace
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from ...database import get_db
from ...models.social_post import SocialPost
from ...models.vehicle import Vehicle
from ...models.facebook_account import FacebookAccount
from ...schemas.facebook import (
    FacebookPostCreate,
    FacebookPostResponse,
    RepostingSchedule,
    RepostingStatus,
    FacebookAccountCreate,
    FacebookAccountResponse,
    MultiAccountStatus
)
from ...services.facebook_service import FacebookService
from ...services.automation_service import AutomationService

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/status", response_model=RepostingStatus)
async def get_reposting_status(db: Session = Depends(get_db)):
    """Get current Facebook reposting status and statistics"""
    try:
        # Get recent posts count
        recent_posts = db.query(SocialPost).filter(
            SocialPost.platform == "facebook",
            SocialPost.created_at >= datetime.now() - timedelta(days=7)
        ).count()
        
        # Get active vehicles count
        active_vehicles = db.query(Vehicle).filter(
            Vehicle.estatus.in_(["DISPONIBLE", "FOTOS"])
        ).count()
        
        # Get automation status
        automation_service = AutomationService(db)
        automation_status = automation_service.get_facebook_automation_status()
        
        return RepostingStatus(
            is_active=automation_status.get("is_active", False),
            last_posted=automation_status.get("last_posted"),
            posts_last_week=recent_posts,
            active_vehicles=active_vehicles,
            next_scheduled=automation_status.get("next_scheduled"),
            total_posts=automation_status.get("total_posts", 0)
        )
    except Exception as e:
        logger.error(f"Error getting reposting status: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving reposting status")

@router.get("/accounts/status", response_model=MultiAccountStatus)
async def get_accounts_status(db: Session = Depends(get_db)):
    """Get status of all Facebook accounts"""
    try:
        accounts = db.query(FacebookAccount).all()
        
        total_accounts = len(accounts)
        manual_accounts = len([a for a in accounts if a.account_type == "manual"])
        auto_accounts = len([a for a in accounts if a.account_type == "auto"])
        active_accounts = len([a for a in accounts if a.is_active])
        configured_accounts = len([a for a in accounts if a.is_configured()])
        
        return MultiAccountStatus(
            accounts=[FacebookAccountResponse(
                id=account.id,
                name=account.name,
                account_type=account.account_type,
                is_active=account.is_active,
                is_configured=account.is_configured(),
                automation_config=account.get_automation_config()
            ) for account in accounts],
            total_accounts=total_accounts,
            manual_accounts=manual_accounts,
            auto_accounts=auto_accounts,
            active_accounts=active_accounts,
            configured_accounts=configured_accounts
        )
    except Exception as e:
        logger.error(f"Error getting accounts status: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving accounts status")

@router.get("/accounts/{account_id}", response_model=FacebookAccountResponse)
async def get_account(account_id: int, db: Session = Depends(get_db)):
    """Get specific Facebook account details"""
    try:
        account = db.query(FacebookAccount).filter(FacebookAccount.id == account_id).first()
        
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        return FacebookAccountResponse(
            id=account.id,
            name=account.name,
            account_type=account.account_type,
            is_active=account.is_active,
            is_configured=account.is_configured(),
            automation_config=account.get_automation_config()
        )
    except Exception as e:
        logger.error(f"Error getting account {account_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving account")

@router.post("/accounts", response_model=FacebookAccountResponse)
async def create_account(
    account_data: FacebookAccountCreate,
    db: Session = Depends(get_db)
):
    """Create a new Facebook account"""
    try:
        account = FacebookAccount(
            name=account_data.name,
            account_type=account_data.account_type,
            access_token=account_data.access_token,
            page_id=account_data.page_id,
            user_id=account_data.user_id,
            app_id=account_data.app_id,
            app_secret=account_data.app_secret,
            automation_config=account_data.automation_config
        )
        
        db.add(account)
        db.commit()
        db.refresh(account)
        
        return FacebookAccountResponse(
            id=account.id,
            name=account.name,
            account_type=account.account_type,
            is_active=account.is_active,
            is_configured=account.is_configured(),
            automation_config=account.get_automation_config()
        )
    except Exception as e:
        logger.error(f"Error creating account: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating account")

@router.put("/accounts/{account_id}", response_model=FacebookAccountResponse)
async def update_account(
    account_id: int,
    account_data: FacebookAccountCreate,
    db: Session = Depends(get_db)
):
    """Update Facebook account"""
    try:
        account = db.query(FacebookAccount).filter(FacebookAccount.id == account_id).first()
        
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Update fields
        account.name = account_data.name
        account.account_type = account_data.account_type
        account.access_token = account_data.access_token
        account.page_id = account_data.page_id
        account.user_id = account_data.user_id
        account.app_id = account_data.app_id
        account.app_secret = account_data.app_secret
        account.automation_config = account_data.automation_config
        
        db.commit()
        db.refresh(account)
        
        return FacebookAccountResponse(
            id=account.id,
            name=account.name,
            account_type=account.account_type,
            is_active=account.is_active,
            is_configured=account.is_configured(),
            automation_config=account.get_automation_config()
        )
    except Exception as e:
        logger.error(f"Error updating account {account_id}: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating account")

@router.post("/accounts/{account_id}/manual-post", response_model=FacebookPostResponse)
async def create_manual_post(
    account_id: int,
    post_data: FacebookPostCreate,
    db: Session = Depends(get_db)
):
    """Create a manual post for a specific account"""
    try:
        account = db.query(FacebookAccount).filter(FacebookAccount.id == account_id).first()
        
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        if not account.is_configured():
            raise HTTPException(status_code=400, detail="Account not configured")
        
        # Get vehicle for the post
        vehicle = db.query(Vehicle).filter(Vehicle.id == post_data.vehicle_id).first()
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        
        # Create post using Facebook service with account credentials
        facebook_service = FacebookService(account_id=account_id, db_session=db)
        result = facebook_service.post_to_facebook(vehicle, post_data.message)
        
        if result.get("error"):
            raise HTTPException(status_code=500, detail=f"Facebook API error: {result['error']}")
        
        # Save to database
        db_post = SocialPost(
            vehicle_id=vehicle.id,
            platform="facebook",
            account_id=account_id,
            message=post_data.message,
            status="posted",
            posted_at=datetime.now(),
            external_post_id=result.get("post_id")
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        
        return FacebookPostResponse(
            id=db_post.id,
            vehicle_id=db_post.vehicle_id,
            platform=db_post.platform,
            message=db_post.message,
            status=db_post.status,
            posted_at=db_post.posted_at,
            external_post_id=db_post.external_post_id,
            account_id=db_post.account_id
        )
        
    except Exception as e:
        logger.error(f"Error creating manual post: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating manual post")

@router.post("/schedule", response_model=RepostingSchedule)
async def schedule_reposting(
    schedule: RepostingSchedule,
    db: Session = Depends(get_db)
):
    """Schedule daily Facebook reposting"""
    try:
        automation_service = AutomationService(db)
        result = automation_service.schedule_facebook_reposting(schedule)
        return result
    except Exception as e:
        logger.error(f"Error scheduling reposting: {e}")
        raise HTTPException(status_code=500, detail="Error scheduling reposting")

@router.post("/test-post", response_model=FacebookPostResponse)
async def test_facebook_post(
    post_data: FacebookPostCreate,
    db: Session = Depends(get_db)
):
    """Test Facebook post with sample vehicle"""
    try:
        facebook_service = FacebookService()
        
        # Get a sample vehicle for testing
        sample_vehicle = db.query(Vehicle).filter(
            Vehicle.estatus == "DISPONIBLE"
        ).first()
        
        if not sample_vehicle:
            raise HTTPException(status_code=404, detail="No available vehicles for testing")
        
        # Create test post
        test_post = facebook_service.create_test_post(sample_vehicle, post_data.message)
        
        # Save to database
        db_post = SocialPost(
            vehicle_id=sample_vehicle.id,
            platform="facebook",
            account_id=post_data.account_id or 1,  # Default to first account
            message=post_data.message,
            status="test",
            posted_at=datetime.now()
        )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        
        return FacebookPostResponse(
            id=db_post.id,
            vehicle_id=db_post.vehicle_id,
            platform=db_post.platform,
            message=db_post.message,
            status=db_post.status,
            posted_at=db_post.posted_at,
            external_post_id=test_post.get("post_id"),
            account_id=db_post.account_id
        )
        
    except Exception as e:
        logger.error(f"Error creating test post: {e}")
        raise HTTPException(status_code=500, detail="Error creating test post")

@router.post("/start-automation")
async def start_facebook_automation(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Start Facebook automation service"""
    try:
        automation_service = AutomationService(db)
        background_tasks.add_task(automation_service.start_facebook_automation)
        
        return {"message": "Facebook automation started successfully"}
    except Exception as e:
        logger.error(f"Error starting automation: {e}")
        raise HTTPException(status_code=500, detail="Error starting automation")

@router.post("/stop-automation")
async def stop_facebook_automation(db: Session = Depends(get_db)):
    """Stop Facebook automation service"""
    try:
        automation_service = AutomationService(db)
        automation_service.stop_facebook_automation()
        
        return {"message": "Facebook automation stopped successfully"}
    except Exception as e:
        logger.error(f"Error stopping automation: {e}")
        raise HTTPException(status_code=500, detail="Error stopping automation")

@router.get("/posts", response_model=List[FacebookPostResponse])
async def get_facebook_posts(
    limit: int = 50,
    offset: int = 0,
    account_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get Facebook posts history"""
    try:
        query = db.query(SocialPost).filter(SocialPost.platform == "facebook")
        
        if account_id:
            query = query.filter(SocialPost.account_id == account_id)
        
        posts = query.order_by(SocialPost.created_at.desc()).offset(offset).limit(limit).all()
        
        return [
            FacebookPostResponse(
                id=post.id,
                vehicle_id=post.vehicle_id,
                platform=post.platform,
                message=post.message,
                status=post.status,
                posted_at=post.posted_at,
                external_post_id=post.external_post_id,
                account_id=post.account_id
            ) for post in posts
        ]
    except Exception as e:
        logger.error(f"Error retrieving Facebook posts: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving posts")

@router.delete("/posts/{post_id}")
async def delete_facebook_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    """Delete a Facebook post"""
    try:
        post = db.query(SocialPost).filter(
            SocialPost.id == post_id,
            SocialPost.platform == "facebook"
        ).first()
        
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        # Delete from Facebook if external ID exists
        if post.external_post_id:
            facebook_service = FacebookService()
            facebook_service.delete_post(post.external_post_id)
        
        # Mark as deleted in database
        post.status = "deleted"
        post.removed_at = datetime.now()
        db.commit()
        
        return {"message": "Post deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting post: {e}")
        raise HTTPException(status_code=500, detail="Error deleting post")
