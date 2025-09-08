"""
Market Intelligence Model
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class MarketIntelligence(Base):
    """Market intelligence model"""
    
    __tablename__ = "market_intelligence"
    
    id = Column(Integer, primary_key=True, index=True)
    data_type = Column(String(100), index=True)
    source = Column(String(255))
    data = Column(JSON)
    collected_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<MarketIntelligence(id={self.id}, data_type='{self.data_type}')>"
