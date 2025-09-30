"""
Database Models Package
"""

from .vehicle import Vehicle
from .photo import Photo
from .status_history import StatusHistory
from .social_post import SocialPost
from .marketplace_listing import MarketplaceListing
from .user import User
from .api_key import ApiKey
from .automation_workflow import AutomationWorkflow
from .workflow_execution import WorkflowExecution
from .analytics_data import AnalyticsData
from .market_intelligence import MarketIntelligence
from .facebook_account import FacebookAccount

# TODO: Set up relationships after all models are imported
# This will be done when we have a working database setup

__all__ = [
    "Vehicle",
    "Photo", 
    "StatusHistory",
    "SocialPost",
    "MarketplaceListing",
    "User",
    "ApiKey",
    "AutomationWorkflow",
    "WorkflowExecution",
    "AnalyticsData",
    "MarketIntelligence",
    "FacebookAccount"
]
