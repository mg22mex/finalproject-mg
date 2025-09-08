"""
Facebook Account Model - Manages multiple Facebook accounts with different automation modes
"""

from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, Dict, Any

from ..database import Base

class FacebookAccount(Base):
    """Facebook account model for multiple account support"""
    
    __tablename__ = "facebook_accounts"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Account information
    name = Column(String(255), nullable=False)
    account_type = Column(String(50), nullable=False, default="manual")  # 'manual' or 'auto'
    is_active = Column(Boolean, default=True)
    
    # Facebook API credentials
    access_token = Column(String(1000))
    page_id = Column(String(255))
    user_id = Column(String(255))
    app_id = Column(String(255))
    app_secret = Column(String(255))
    
    # Automation configuration
    automation_config = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    social_posts = relationship("SocialPost", back_populates="facebook_account")
    
    def __repr__(self):
        return f"<FacebookAccount(id={self.id}, name='{self.name}', type='{self.account_type}')>"
    
    def is_configured(self) -> bool:
        """Check if account has required credentials"""
        return bool(self.access_token and self.page_id)
    
    def is_manual(self) -> bool:
        """Check if account is manual-only"""
        return self.account_type == "manual"
    
    def is_auto(self) -> bool:
        """Check if account supports automation"""
        return self.account_type == "auto"
    
    def get_automation_config(self) -> Dict[str, Any]:
        """Get automation configuration with defaults"""
        config = self.automation_config or {}
        return {
            "auto_posting": config.get("auto_posting", False),
            "schedule": {
                "time": config.get("schedule", {}).get("time", "09:00"),
                "days": config.get("schedule", {}).get("days", [1, 2, 3, 4, 5]),
                "max_posts_per_day": config.get("schedule", {}).get("max_posts_per_day", 3)
            }
        }
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "name": self.name,
            "account_type": self.account_type,
            "is_active": self.is_active,
            "is_configured": self.is_configured(),
            "automation_config": self.get_automation_config(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
