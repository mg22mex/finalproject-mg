"""
Facebook Reposting Pydantic Schemas
Data validation and serialization for Facebook automation
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class PostStatus(str, Enum):
    """Facebook post status enumeration"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    POSTED = "posted"
    FAILED = "failed"
    DELETED = "deleted"
    TEST = "test"

class PlatformType(str, Enum):
    """Social media platform types"""
    FACEBOOK = "facebook"
    MARKETPLACE = "marketplace"
    INSTAGRAM = "instagram"

class FacebookPostCreate(BaseModel):
    """Schema for creating a Facebook post"""
    message: str = Field(..., min_length=10, max_length=5000, description="Post message content")
    vehicle_id: Optional[int] = Field(None, description="Vehicle ID to post about")
    platform: PlatformType = Field(PlatformType.FACEBOOK, description="Platform to post to")
    account_id: Optional[int] = Field(None, description="Facebook account ID to post from")
    scheduled_time: Optional[datetime] = Field(None, description="When to schedule the post")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "¡Excelente oportunidad! Toyota Camry 2020 en perfecto estado, solo 45,000 km. Precio especial: $250,000. ¡Llámanos hoy mismo!",
                "vehicle_id": 1,
                "platform": "facebook",
                "account_id": 1,
                "scheduled_time": "2024-01-15T10:00:00Z"
            }
        }

class FacebookPostResponse(BaseModel):
    """Schema for Facebook post response"""
    id: int
    vehicle_id: int
    platform: str
    message: str
    status: str
    posted_at: Optional[datetime]
    external_post_id: Optional[str] = None
    account_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class RepostingSchedule(BaseModel):
    """Schema for scheduling daily reposting"""
    is_active: bool = Field(True, description="Enable/disable daily reposting")
    time_of_day: str = Field("09:00", description="Time to post daily (24h format)")
    days_of_week: List[int] = Field([0,1,2,3,4,5,6], description="Days to post (0=Sunday, 1=Monday, etc.)")
    max_posts_per_day: int = Field(5, description="Maximum posts per day")
    post_interval_hours: int = Field(4, description="Hours between posts")
    include_marketplace: bool = Field(True, description="Also post to Facebook Marketplace")
    
    class Config:
        json_schema_extra = {
            "example": {
                "is_active": True,
                "time_of_day": "09:00",
                "days_of_week": [1,2,3,4,5],
                "max_posts_per_day": 5,
                "post_interval_hours": 4,
                "include_marketplace": True
            }
        }

class RepostingStatus(BaseModel):
    """Schema for reposting service status"""
    is_active: bool
    last_posted: Optional[datetime] = None
    posts_last_week: int = 0
    active_vehicles: int = 0
    next_scheduled: Optional[datetime] = None
    total_posts: int = 0
    
    class Config:
        from_attributes = True

class FacebookCredentials(BaseModel):
    """Schema for Facebook API credentials"""
    access_token: str = Field(..., description="Facebook access token")
    page_id: str = Field(..., description="Facebook page ID")
    user_id: str = Field(..., description="Facebook user ID")
    app_id: str = Field(..., description="Facebook app ID")
    app_secret: str = Field(..., description="Facebook app secret")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "EAABwzLixnjYBO...",
                "page_id": "123456789012345",
                "user_id": "987654321098765",
                "app_id": "123456789012345",
                "app_secret": "abcdef123456789..."
            }
        }

class PostTemplate(BaseModel):
    """Schema for post content templates"""
    name: str = Field(..., description="Template name")
    content: str = Field(..., description="Template content with placeholders")
    variables: List[str] = Field(..., description="Available variables for this template")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Vehicle Sale Template",
                "content": "¡{marca} {modelo} {año} en {ubicacion}! Solo {kilometraje} km. Precio especial: ${precio}. ¡Llámanos hoy!",
                "variables": ["marca", "modelo", "año", "ubicacion", "kilometraje", "precio"]
            }
        }

class FacebookAccountCreate(BaseModel):
    """Schema for creating a Facebook account"""
    name: str = Field(..., description="Account name")
    account_type: str = Field(..., description="Account type: manual or auto")
    access_token: Optional[str] = Field(None, description="Facebook access token")
    page_id: Optional[str] = Field(None, description="Facebook page ID")
    user_id: Optional[str] = Field(None, description="Facebook user ID")
    app_id: Optional[str] = Field(None, description="Facebook app ID")
    app_secret: Optional[str] = Field(None, description="Facebook app secret")
    automation_config: Optional[dict] = Field(None, description="Automation configuration")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Auto Account 1",
                "account_type": "auto",
                "access_token": "EAABwzLixnjYBO...",
                "page_id": "123456789012345",
                "automation_config": {
                    "auto_posting": True,
                    "schedule": {
                        "time": "09:00",
                        "days": [1, 2, 3, 4, 5],
                        "max_posts_per_day": 3
                    }
                }
            }
        }

class FacebookAccountResponse(BaseModel):
    """Schema for Facebook account response"""
    id: int
    name: str
    account_type: str
    is_active: bool
    is_configured: bool
    automation_config: dict
    
    class Config:
        from_attributes = True

class MultiAccountStatus(BaseModel):
    """Schema for multi-account status"""
    accounts: List[FacebookAccountResponse]
    total_accounts: int
    manual_accounts: int
    auto_accounts: int
    active_accounts: int
    configured_accounts: int
    
    class Config:
        from_attributes = True
