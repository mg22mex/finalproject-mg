"""
Automation Workflow Model
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.sql import func

from ..database import Base

class AutomationWorkflow(Base):
    """Automation workflow model"""
    
    __tablename__ = "automation_workflows"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    workflow_type = Column(String(100), index=True)
    is_active = Column(Boolean, default=True)
    config = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<AutomationWorkflow(id={self.id}, name='{self.name}')>"
