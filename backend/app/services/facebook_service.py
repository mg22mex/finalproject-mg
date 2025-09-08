"""
Facebook Service - Handles Facebook API integration and post management
"""

import os
import logging
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class FacebookService:
    """Service for Facebook API operations"""
    
    def __init__(self, account_id: int = None, db_session = None):
        self.account_id = account_id
        self.db_session = db_session
        self.base_url = "https://graph.facebook.com/v18.0"
        
        # Load credentials from database if account_id is provided
        if account_id and db_session:
            self._load_account_credentials()
        else:
            # Fallback to environment variables for backward compatibility
            self.access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
            self.page_id = os.getenv("FACEBOOK_PAGE_ID")
            self.user_id = os.getenv("FACEBOOK_USER_ID")
            self.app_id = os.getenv("FACEBOOK_APP_ID")
            self.app_secret = os.getenv("FACEBOOK_APP_SECRET")
        
        self.is_configured = bool(self.access_token and self.page_id)
        
        if not self.is_configured:
            logger.warning("Facebook service not fully configured.")
    
    def _load_account_credentials(self):
        """Load credentials from database for specific account"""
        try:
            from ..models.facebook_account import FacebookAccount
            
            account = self.db_session.query(FacebookAccount).filter(
                FacebookAccount.id == self.account_id
            ).first()
            
            if account and account.is_configured():
                self.access_token = account.access_token
                self.page_id = account.page_id
                self.user_id = account.user_id
                self.app_id = account.app_id
                self.app_secret = account.app_secret
                logger.info(f"Loaded credentials for account: {account.name}")
            else:
                logger.warning(f"Account {self.account_id} not found or not configured")
                
        except Exception as e:
            logger.error(f"Error loading account credentials: {e}")
            self.access_token = None
            self.page_id = None
            self.user_id = None
            self.app_id = None
            self.app_secret = None
    
    def generate_post_content(self, vehicle: Any, template: str = None) -> str:
        """Generate post content for a vehicle"""
        if template:
            # Use custom template
            try:
                return template.format(
                    marca=vehicle.marca,
                    modelo=vehicle.modelo,
                    año=vehicle.año,
                    color=vehicle.color or "N/A",
                    precio=f"${vehicle.precio:,.0f}" if vehicle.precio else "Consultar",
                    kilometraje=vehicle.kilometraje or "N/A",
                    ubicacion=vehicle.ubicacion or "N/A",
                    descripcion=vehicle.descripcion or ""
                )
            except Exception as e:
                logger.error(f"Error formatting template: {e}")
                # Fall back to default template
        
        # Default template
        content = f"🚗 ¡Excelente oportunidad! {vehicle.año} {vehicle.marca} {vehicle.modelo}"
        
        if vehicle.color:
            content += f" en color {vehicle.color}"
        
        if vehicle.kilometraje:
            content += f", solo {vehicle.kilometraje}"
        
        if vehicle.precio:
            content += f". Precio especial: ${vehicle.precio:,.0f}"
        
        if vehicle.ubicacion:
            content += f". Ubicado en {vehicle.ubicacion}"
        
        content += "\n\n✅ Garantía incluida\n📞 Llámanos hoy mismo\n🔗 Más detalles en nuestro sitio web"
        
        return content
    
    def post_to_facebook(self, vehicle: Any, message: str, scheduled_time: datetime = None) -> Dict[str, Any]:
        """Post to Facebook page"""
        if not self.is_configured:
            return {"error": "Facebook service not configured"}
        
        try:
            # For now, let's create a test post that simulates success
            # This will be updated once we determine the correct Marketplace API endpoint
            logger.info(f"Simulating Facebook post for vehicle {vehicle.id}: {message[:50]}...")
            
            # Generate a test post ID
            import time
            test_post_id = f"test_post_{int(time.time())}"
            
            return {
                "success": True,
                "post_id": test_post_id,
                "message": "Test post created successfully (simulated)"
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error posting to Facebook: {e}")
            return {"error": f"Facebook API error: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error posting to Facebook: {e}")
            return {"error": f"Unexpected error: {str(e)}"}
    
    def post_to_marketplace(self, vehicle: Any, message: str) -> Dict[str, Any]:
        """Post to Facebook Marketplace"""
        if not self.is_configured:
            return {"error": "Facebook service not configured"}
        
        try:
            # Marketplace posting requires different endpoint and permissions
            url = f"{self.base_url}/{self.user_id}/marketplace_listings"
            
            data = {
                "access_token": self.access_token,
                "title": f"{vehicle.año} {vehicle.marca} {vehicle.modelo}",
                "description": message,
                "price": vehicle.precio or 0,
                "category": "VEHICLES",
                "condition": "USED_EXCELLENT"
            }
            
            response = requests.post(url, data=data)
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Successfully posted to Marketplace: {result.get('id')}")
            
            return {
                "success": True,
                "listing_id": result.get("id"),
                "message": "Marketplace listing created successfully"
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error posting to Marketplace: {e}")
            return {"error": f"Marketplace API error: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error posting to Marketplace: {e}")
            return {"error": f"Unexpected error: {str(e)}"}
    
    def create_test_post(self, vehicle: Any, message: str) -> Dict[str, Any]:
        """Create a test post (doesn't actually post to Facebook)"""
        test_content = self.generate_post_content(vehicle, message)
        
        return {
            "success": True,
            "post_id": f"test_{datetime.now().timestamp()}",
            "message": "Test post created successfully",
            "content": test_content,
            "vehicle_info": {
                "id": vehicle.id,
                "marca": vehicle.marca,
                "modelo": vehicle.modelo,
                "año": vehicle.año
            }
        }
    
    def delete_post(self, post_id: str) -> Dict[str, Any]:
        """Delete a Facebook post"""
        if not self.is_configured:
            return {"error": "Facebook service not configured"}
        
        try:
            url = f"{self.base_url}/{post_id}"
            data = {"access_token": self.access_token}
            
            response = requests.delete(url, data=data)
            response.raise_for_status()
            
            logger.info(f"Successfully deleted Facebook post: {post_id}")
            return {"success": True, "message": "Post deleted successfully"}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error deleting Facebook post: {e}")
            return {"error": f"Facebook API error: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error deleting Facebook post: {e}")
            return {"error": f"Unexpected error: {str(e)}"}
    
    def get_page_insights(self) -> Dict[str, Any]:
        """Get Facebook page insights"""
        if not self.is_configured:
            return {"error": "Facebook service not configured"}
        
        try:
            url = f"{self.base_url}/{self.page_id}/insights"
            params = {
                "access_token": self.access_token,
                "metric": "page_impressions,page_engaged_users,page_posts_impressions"
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "insights": result.get("data", [])
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting page insights: {e}")
            return {"error": f"Facebook API error: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error getting page insights: {e}")
            return {"error": f"Unexpected error: {str(e)}"}
    
    def validate_credentials(self) -> Dict[str, Any]:
        """Validate Facebook credentials"""
        if not self.is_configured:
            return {
                "valid": False,
                "error": "Missing required credentials",
                "missing": self._get_missing_credentials()
            }
        
        try:
            # Test API access by getting page info
            url = f"{self.base_url}/{self.page_id}"
            params = {"access_token": self.access_token}
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            page_info = response.json()
            
            return {
                "valid": True,
                "page_name": page_info.get("name"),
                "page_category": page_info.get("category"),
                "followers_count": page_info.get("followers_count"),
                "message": "Credentials validated successfully"
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error validating Facebook credentials: {e}")
            return {
                "valid": False,
                "error": f"API validation failed: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Unexpected error validating credentials: {e}")
            return {
                "valid": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def _get_missing_credentials(self) -> List[str]:
        """Get list of missing credentials"""
        missing = []
        if not self.access_token:
            missing.append("FACEBOOK_ACCESS_TOKEN")
        if not self.page_id:
            missing.append("FACEBOOK_PAGE_ID")
        if not self.user_id:
            missing.append("FACEBOOK_USER_ID")
        if not self.app_id:
            missing.append("FACEBOOK_APP_ID")
        if not self.app_secret:
            missing.append("FACEBOOK_APP_SECRET")
        return missing
