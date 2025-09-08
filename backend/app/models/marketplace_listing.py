"""
Marketplace Listing Model - Manages Facebook Marketplace listings
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional

Base = declarative_base()

class MarketplaceListing(Base):
    """Marketplace listing model"""
    
    __tablename__ = "marketplace_listings"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    platform = Column(String(50), default="marketplace")
    listing_id = Column(String(255))
    external_listing_id = Column(String(255))
    status = Column(String(50), default="active", index=True)
    posted_at = Column(DateTime(timezone=True))
    removed_at = Column(DateTime(timezone=True))
    repost_count = Column(Integer, default=0)
    last_repost_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    vehicle = relationship("Vehicle", back_populates="marketplace_listings")
    
    def __repr__(self):
        return f"<MarketplaceListing(id={self.id}, vehicle_id={self.vehicle_id}, status={self.status})>"
