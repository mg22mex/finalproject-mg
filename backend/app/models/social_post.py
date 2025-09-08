"""
Social Post Model - Manages social media posts for vehicles
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, Dict, Any

from ..database import Base

class SocialPost(Base):
    """Social media post model"""
    
    __tablename__ = "social_posts"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    account_id = Column(Integer, ForeignKey("facebook_accounts.id"), nullable=True, index=True)
    
    # Platform information
    platform = Column(String(50), nullable=False, index=True)
    post_id = Column(String(255))
    external_post_id = Column(String(255))
    
    # Post content
    message = Column(Text)
    status = Column(String(50), default="active", index=True)
    
    # Timing
    posted_at = Column(DateTime(timezone=True))
    removed_at = Column(DateTime(timezone=True))
    
    # Engagement metrics
    engagement_metrics = Column(JSON)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    vehicle = relationship("Vehicle", back_populates="social_posts")
    facebook_account = relationship("FacebookAccount", back_populates="social_posts")
    
    def __repr__(self):
        return f"<SocialPost(id={self.id}, platform={self.platform}, status={self.status})>"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "vehicle_id": self.vehicle_id,
            "platform": self.platform.value if self.platform else None,
            "post_id": self.post_id,
            "external_post_id": self.external_post_id,
            "message": self.message,
            "status": self.status.value if self.status else None,
            "posted_at": self.posted_at.isoformat() if self.posted_at else None,
            "removed_at": self.removed_at.isoformat() if self.removed_at else None,
            "engagement_metrics": self.engagement_metrics,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
