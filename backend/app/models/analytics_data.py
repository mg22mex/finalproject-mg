"""
Analytics Data Model
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class AnalyticsData(Base):
    """Analytics data model"""
    
    __tablename__ = "analytics_data"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), index=True)
    data_type = Column(String(100), index=True)
    data = Column(JSON)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    vehicle = relationship("Vehicle", back_populates="analytics_data")
    
    def __repr__(self):
        return f"<AnalyticsData(id={self.id}, vehicle_id={self.vehicle_id})>"
