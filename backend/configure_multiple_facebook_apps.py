#!/usr/bin/env python3
"""
Configure Multiple Facebook Apps for Autosell.mx
This script helps configure Facebook apps for multiple accounts
"""

import os
import sys
import requests
from typing import Dict, Any, Optional
import json

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db
from app.models.facebook_account import FacebookAccount

class FacebookAppConfigurator:
    """Helper class to configure multiple Facebook apps"""
    
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v18.0"
        
    def create_facebook_app_guide(self, account_name: str, account_type: str) -> Dict[str, Any]:
        """Generate step-by-step guide for creating Facebook app"""
        
        guide = {
            "account_name": account_name,
            "account_type": account_type,
            "steps": [
                {
                    "step": 1,
                    "title": "Access Facebook Developer Console",
                    "description": f"Log into Facebook Developer Console with your {account_name} credentials",
                    "url": "https://developers.facebook.com",
                    "action": "Navigate to the new interface and look for 'Create App' or 'My Apps' option"
                },
                {
                    "step": 2,
                    "title": "Create New App",
                    "description": "Create a new Facebook app for this account",
                    "details": {
                        "app_type": "Business App (recommended for Autosell.mx)",
                        "app_name": f"Autosell-{account_name.replace(' ', '')}-2025",
                        "contact_email": f"Your {account_name} email address",
                        "business_account": "Select your business account",
                        "note": "Choose 'Business App' from the available options"
                    }
                },
                {
                    "step": 3,
                    "title": "Add Required Products",
                    "description": "Add necessary products to your app",
                    "action": "Look for 'Products' section and add:",
                    "products": [
                        "Facebook Login - For user authentication",
                        "Pages API - For posting to Facebook pages",
                        "Marketing API - For advanced features (optional)"
                    ]
                },
                {
                    "step": 4,
                    "title": "Configure OAuth Redirect URIs",
                    "description": "Set up OAuth redirect URIs for your app",
                    "redirect_uris": [
                        "https://autosell-backend.onrender.com/auth/facebook/callback",
                        "http://localhost:8000/auth/facebook/callback"
                    ]
                },
                {
                    "step": 5,
                    "title": "Add App Domains",
                    "description": "Configure app domains for your app",
                    "domains": [
                        "autosell-backend.onrender.com"
                    ]
                },
                {
                    "step": 6,
                    "title": "Get App Credentials",
                    "description": "Copy App ID and App Secret from the app dashboard",
                    "credentials": {
                        "app_id": "Copy from App Dashboard",
                        "app_secret": "Copy from App Dashboard"
                    }
                },
                {
                    "step": 7,
                    "title": "Configure App Permissions",
                    "description": "Request necessary permissions for your app",
                    "permissions": [
                        "pages_manage_posts",
                        "pages_read_engagement",
                        "pages_show_list",
                        "publish_to_groups",
                        "user_posts"
                    ]
                }
            ]
        }
        
        return guide
    
    def generate_app_configuration_script(self, account_name: str, app_id: str, app_secret: str) -> str:
        """Generate Python script to configure the Facebook account"""
        
        script = f'''#!/usr/bin/env python3
"""
Configure Facebook Account: {account_name}
Generated configuration script
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db
from app.models.facebook_account import FacebookAccount

def configure_{account_name.lower().replace(' ', '_')}_account():
    """Configure {account_name} Facebook account"""
    
    # Database session
    db = next(get_db())
    
    try:
        # Check if account already exists
        existing_account = db.query(FacebookAccount).filter(
            FacebookAccount.name == "{account_name}"
        ).first()
        
        if existing_account:
            print(f"Account '{{existing_account.name}}' already exists. Updating...")
            account = existing_account
        else:
            print(f"Creating new account: {account_name}")
            account = FacebookAccount(
                name="{account_name}",
                account_type="auto"  # or "manual" for manual account
            )
            db.add(account)
        
        # Update credentials
        account.app_id = "{app_id}"
        account.app_secret = "{app_secret}"
        account.is_active = True
        
        # Commit changes
        db.commit()
        
        print(f"✅ {account_name} account configured successfully!")
        print(f"   App ID: {app_id}")
        print(f"   App Secret: {app_secret[:8]}...")
        print(f"   Account ID: {{account.id}}")
        
        return account.id
        
    except Exception as e:
        print(f"❌ Error configuring {account_name}: {{str(e)}}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    account_id = configure_{account_name.lower().replace(' ', '_')}_account()
    if account_id:
        print(f"\\n🎉 {account_name} Facebook account configured with ID: {{account_id}}")
    else:
        print(f"\\n❌ Failed to configure {account_name} Facebook account")
'''
        
        return script
    
    def print_setup_guide(self, account_name: str, account_type: str):
        """Print step-by-step setup guide"""
        
        guide = self.create_facebook_app_guide(account_name, account_type)
        
        print(f"\n🚀 Facebook App Setup Guide for {account_name}")
        print("=" * 60)
        
        for step in guide["steps"]:
            print(f"\n📋 Step {step['step']}: {step['title']}")
            print(f"   {step['description']}")
            
            if "action" in step:
                print(f"   Action: {step['action']}")
            
            if "details" in step:
                print("   Details:")
                for key, value in step["details"].items():
                    print(f"     {key}: {value}")
            
            if "redirect_uris" in step:
                print("   Redirect URIs:")
                for uri in step["redirect_uris"]:
                    print(f"     - {uri}")
            
            if "domains" in step:
                print("   Domains:")
                for domain in step["domains"]:
                    print(f"     - {domain}")
            
            if "permissions" in step:
                print("   Required Permissions:")
                for permission in step["permissions"]:
                    print(f"     - {permission}")
            
            if "credentials" in step:
                print("   Credentials to collect:")
                for key, value in step["credentials"].items():
                    print(f"     {key}: {value}")
        
        print(f"\n✅ Once you have the App ID and App Secret, run:")
        print(f"   python configure_{account_name.lower().replace(' ', '_')}_account.py")
        print("=" * 60)

def main():
    """Main function to generate setup guides"""
    
    configurator = FacebookAppConfigurator()
    
    # Define the accounts to configure
    accounts = [
        {"name": "Auto Account 1", "type": "auto"},
        {"name": "Auto Account 2", "type": "auto"}
    ]
    
    print("🚗 Autosell.mx - Multiple Facebook App Configuration")
    print("=" * 60)
    print("This script will help you set up Facebook apps for multiple accounts.")
    print("Each account needs its own Facebook app for proper integration.")
    print("=" * 60)
    
    for account in accounts:
        configurator.print_setup_guide(account["name"], account["type"])
        
        # Generate configuration script
        script_content = configurator.generate_app_configuration_script(
            account["name"], 
            "YOUR_APP_ID_HERE", 
            "YOUR_APP_SECRET_HERE"
        )
        
        # Save script to file
        script_filename = f"configure_{account['name'].lower().replace(' ', '_')}_account.py"
        with open(script_filename, 'w') as f:
            f.write(script_content)
        
        print(f"\n📝 Configuration script saved: {script_filename}")
        print("   Edit the script and replace YOUR_APP_ID_HERE and YOUR_APP_SECRET_HERE")
        print("   with your actual Facebook app credentials.")
    
    print(f"\n🎯 Next Steps:")
    print("1. Follow the setup guides above for each account")
    print("2. Create Facebook apps for each account")
    print("3. Get App ID and App Secret for each app")
    print("4. Update the configuration scripts with real credentials")
    print("5. Run the configuration scripts to set up your accounts")
    print("6. Test the Facebook integration for each account")
    
    print(f"\n✅ All setup guides and scripts generated successfully!")

if __name__ == "__main__":
    main()
