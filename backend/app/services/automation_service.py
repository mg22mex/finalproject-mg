"""
Automation Service - Manages daily Facebook reposting automation
"""

import os
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import json

from ..models.automation_workflow import AutomationWorkflow
from ..models.vehicle import Vehicle
from ..models.social_post import SocialPost
from .facebook_service import FacebookService

logger = logging.getLogger(__name__)

class AutomationService:
    """Service for managing automation workflows"""
    
    def __init__(self, db_session):
        self.db = db_session
        self.facebook_service = FacebookService()
        self.is_running = False
        self.scheduler_task = None
        
    def get_facebook_automation_status(self) -> Dict[str, Any]:
        """Get current Facebook automation status"""
        try:
            # Get automation workflow
            workflow = self.db.query(AutomationWorkflow).filter(
                AutomationWorkflow.workflow_type == "facebook_reposting"
            ).first()
            
            if not workflow:
                return {
                    "is_active": False,
                    "last_posted": None,
                    "next_scheduled": None,
                    "total_posts": 0,
                    "message": "No automation workflow configured"
                }
            
            # Get last post time
            last_post = self.db.query(SocialPost).filter(
                SocialPost.platform == "facebook",
                SocialPost.status == "posted"
            ).order_by(SocialPost.posted_at.desc()).first()
            
            # Get total posts
            total_posts = self.db.query(SocialPost).filter(
                SocialPost.platform == "facebook"
            ).count()
            
            # Calculate next scheduled time
            config = workflow.config or {}
            next_scheduled = self._calculate_next_scheduled_time(config)
            
            return {
                "is_active": workflow.is_active and self.is_running,
                "last_posted": last_post.posted_at if last_post else None,
                "next_scheduled": next_scheduled,
                "total_posts": total_posts,
                "workflow_name": workflow.name,
                "config": config
            }
            
        except Exception as e:
            logger.error(f"Error getting automation status: {e}")
            return {
                "is_active": False,
                "error": str(e)
            }
    
    def schedule_facebook_reposting(self, schedule: Dict[str, Any]) -> Dict[str, Any]:
        """Schedule Facebook reposting automation"""
        try:
            # Check if workflow exists
            workflow = self.db.query(AutomationWorkflow).filter(
                AutomationWorkflow.workflow_type == "facebook_reposting"
            ).first()
            
            if workflow:
                # Update existing workflow
                workflow.is_active = schedule.get("is_active", True)
                workflow.config = schedule
                workflow.name = "Facebook Daily Reposting"
            else:
                # Create new workflow
                workflow = AutomationWorkflow(
                    name="Facebook Daily Reposting",
                    workflow_type="facebook_reposting",
                    is_active=schedule.get("is_active", True),
                    config=schedule
                )
                self.db.add(workflow)
            
            self.db.commit()
            
            # Start automation if enabled
            if schedule.get("is_active", False):
                self.start_facebook_automation()
            
            return {
                "success": True,
                "message": "Facebook reposting scheduled successfully",
                "schedule": schedule
            }
            
        except Exception as e:
            logger.error(f"Error scheduling Facebook reposting: {e}")
            self.db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    
    def start_facebook_automation(self):
        """Start Facebook automation service"""
        if self.is_running:
            logger.info("Facebook automation already running")
            return
        
        try:
            self.is_running = True
            logger.info("Starting Facebook automation service")
            
            # Start background scheduler
            asyncio.create_task(self._run_facebook_scheduler())
            
            return {"success": True, "message": "Automation started"}
            
        except Exception as e:
            logger.error(f"Error starting Facebook automation: {e}")
            self.is_running = False
            return {"success": False, "error": str(e)}
    
    def stop_facebook_automation(self):
        """Stop Facebook automation service"""
        try:
            self.is_running = False
            logger.info("Stopping Facebook automation service")
            
            # Cancel scheduler task if running
            if self.scheduler_task:
                self.scheduler_task.cancel()
                self.scheduler_task = None
            
            return {"success": True, "message": "Automation stopped"}
            
        except Exception as e:
            logger.error(f"Error stopping Facebook automation: {e}")
            return {"success": False, "error": str(e)}
    
    async def _run_facebook_scheduler(self):
        """Background task for Facebook reposting scheduler"""
        try:
            while self.is_running:
                # Get current automation status
                status = self.get_facebook_automation_status()
                
                if status.get("is_active") and self._should_post_now(status.get("config", {})):
                    # Execute reposting
                    await self._execute_daily_reposting()
                
                # Wait for next check (every 15 minutes)
                await asyncio.sleep(900)
                
        except asyncio.CancelledError:
            logger.info("Facebook scheduler cancelled")
        except Exception as e:
            logger.error(f"Error in Facebook scheduler: {e}")
            self.is_running = False
    
    def _should_post_now(self, config: Dict[str, Any]) -> bool:
        """Check if it's time to post based on schedule"""
        try:
            if not config.get("is_active", False):
                return False
            
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            current_day = now.weekday()
            
            # Check if current day is in schedule
            if current_day not in config.get("days_of_week", []):
                return False
            
            # Check if current time matches schedule
            if current_time != config.get("time_of_day", "09:00"):
                return False
            
            # Check if we haven't exceeded daily limit
            today_posts = self.db.query(SocialPost).filter(
                SocialPost.platform == "facebook",
                SocialPost.created_at >= now.replace(hour=0, minute=0, second=0, microsecond=0)
            ).count()
            
            max_posts = config.get("max_posts_per_day", 5)
            return today_posts < max_posts
            
        except Exception as e:
            logger.error(f"Error checking post schedule: {e}")
            return False
    
    async def _execute_daily_reposting(self):
        """Execute daily Facebook reposting"""
        try:
            logger.info("Executing daily Facebook reposting")
            
            # Get vehicles that need reposting
            vehicles = self._get_vehicles_for_reposting()
            
            if not vehicles:
                logger.info("No vehicles need reposting today")
                return
            
            # Get automation config
            workflow = self.db.query(AutomationWorkflow).filter(
                AutomationWorkflow.workflow_type == "facebook_reposting"
            ).first()
            
            config = workflow.config if workflow else {}
            
            # Post vehicles
            posted_count = 0
            for vehicle in vehicles[:config.get("max_posts_per_day", 5)]:
                try:
                    # Generate post content
                    message = self.facebook_service.generate_post_content(vehicle)
                    
                    # Post to Facebook
                    result = self.facebook_service.post_to_facebook(vehicle, message)
                    
                    if result.get("success"):
                        # Save to database
                        social_post = SocialPost(
                            vehicle_id=vehicle.id,
                            platform="facebook",
                            message=message,
                            status="posted",
                            posted_at=datetime.now(),
                            external_post_id=result.get("post_id")
                        )
                        self.db.add(social_post)
                        
                        # Post to Marketplace if enabled
                        if config.get("include_marketplace", True):
                            marketplace_result = self.facebook_service.post_to_marketplace(vehicle, message)
                            if marketplace_result.get("success"):
                                logger.info(f"Posted vehicle {vehicle.id} to Marketplace")
                        
                        posted_count += 1
                        logger.info(f"Successfully posted vehicle {vehicle.id} to Facebook")
                        
                    else:
                        logger.error(f"Failed to post vehicle {vehicle.id}: {result.get('error')}")
                        
                except Exception as e:
                    logger.error(f"Error posting vehicle {vehicle.id}: {e}")
                    continue
            
            # Commit all posts
            self.db.commit()
            
            logger.info(f"Daily reposting completed: {posted_count} vehicles posted")
            
        except Exception as e:
            logger.error(f"Error executing daily reposting: {e}")
            self.db.rollback()
    
    def _get_vehicles_for_reposting(self) -> List[Vehicle]:
        """Get vehicles that need reposting"""
        try:
            # Get vehicles that haven't been posted in the last 24 hours
            yesterday = datetime.now() - timedelta(days=1)
            
            # Get all available vehicles
            vehicles = self.db.query(Vehicle).filter(
                Vehicle.estatus.in_(["DISPONIBLE", "FOTOS"])
            ).all()
            
            # Filter vehicles that need reposting
            vehicles_to_repost = []
            
            for vehicle in vehicles:
                # Check if vehicle has been posted recently
                recent_posts = self.db.query(SocialPost).filter(
                    SocialPost.vehicle_id == vehicle.id,
                    SocialPost.platform == "facebook",
                    SocialPost.created_at > yesterday,
                    SocialPost.status == "posted"
                ).count()
                
                # If no recent posts, add to repost list
                if recent_posts == 0:
                    vehicles_to_repost.append(vehicle)
            
            return vehicles_to_repost
            
        except Exception as e:
            logger.error(f"Error getting vehicles for reposting: {e}")
            return []
    
    def _calculate_next_scheduled_time(self, config: Dict[str, Any]) -> Optional[datetime]:
        """Calculate next scheduled posting time"""
        try:
            if not config.get("is_active", False):
                return None
            
            now = datetime.now()
            time_str = config.get("time_of_day", "09:00")
            days = config.get("days_of_week", [1,2,3,4,5])  # Monday to Friday by default
            
            # Parse time
            hour, minute = map(int, time_str.split(":"))
            
            # Find next scheduled day
            current_day = now.weekday()
            next_day = None
            
            for day in sorted(days):
                if day > current_day:
                    next_day = day
                    break
            
            if next_day is None:
                # Next occurrence is next week
                next_day = min(days)
                days_ahead = 7 - current_day + next_day
            else:
                days_ahead = next_day - current_day
            
            # Calculate next scheduled time
            next_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            next_time += timedelta(days=days_ahead)
            
            return next_time
            
        except Exception as e:
            logger.error(f"Error calculating next scheduled time: {e}")
            return None
