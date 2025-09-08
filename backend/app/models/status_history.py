"""
Status History Model - Tracks vehicle status changes
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional

Base = declarative_base()

class StatusHistory(Base):
    """Status history model for tracking vehicle status changes"""
    
    __tablename__ = "status_history"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign key to vehicle
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False, index=True)
    
    # Status information
    old_status = Column(String(50))
    new_status = Column(String(50), nullable=False, index=True)
    
    # Change metadata
    changed_at = Column(DateTime(timezone=True), server_default=func.now())
    changed_by = Column(String(100))
    reason = Column(Text)
    notes = Column(Text)
    
    # Relationships
    vehicle = relationship("Vehicle", back_populates="status_history")
    
    def __repr__(self):
        return f"<StatusHistory(id={self.id}, vehicle_id={self.vehicle_id}, {self.old_status} -> {self.new_status})>"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "vehicle_id": self.vehicle_id,
            "old_status": self.old_status.value if self.old_status else None,
            "new_status": self.new_status.value if self.new_status else None,
            "changed_at": self.changed_at.isoformat() if self.changed_at else None,
            "changed_by": self.changed_by,
            "reason": self.reason,
            "notes": self.notes
        }
