#!/usr/bin/env python3
"""
Test Multiple Facebook Accounts
This script tests Facebook integration for all configured accounts
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db
from app.models.facebook_account import FacebookAccount
from app.services.facebook_service import FacebookService

def test_facebook_accounts():
    """Test all configured Facebook accounts"""
    
    print("🚗 Autosell.mx - Facebook Accounts Test")
    print("=" * 50)
    
    # Get database session
    db = next(get_db())
    
    try:
        # Get all Facebook accounts
        accounts = db.query(FacebookAccount).all()
        
        if not accounts:
            print("❌ No Facebook accounts found in database.")
            print("   Please configure at least one Facebook account first.")
            return
        
        print(f"📊 Found {len(accounts)} Facebook account(s):")
        print()
        
        for account in accounts:
            print(f"🔍 Testing Account: {account.name}")
            print(f"   Type: {account.account_type}")
            print(f"   Active: {account.is_active}")
            print(f"   Configured: {account.is_configured()}")
            
            if account.is_configured():
                # Test the account
                try:
                    facebook_service = FacebookService(account.id, db)
                    
                    if facebook_service.is_configured:
                        print("   ✅ Service configured successfully")
                        
                        # Test basic API call
                        try:
                            # Test getting user info
                            user_info = facebook_service.get_user_info()
                            if user_info:
                                print(f"   ✅ API connection successful")
                                print(f"   👤 User: {user_info.get('name', 'Unknown')}")
                            else:
                                print("   ⚠️  API connection failed - no user info")
                        except Exception as e:
                            print(f"   ❌ API test failed: {str(e)}")
                    else:
                        print("   ❌ Service not properly configured")
                        
                except Exception as e:
                    print(f"   ❌ Error testing account: {str(e)}")
            else:
                print("   ⚠️  Account not fully configured")
                print("   📝 Missing credentials:")
                if not account.access_token:
                    print("     - Access Token")
                if not account.page_id:
                    print("     - Page ID")
                if not account.app_id:
                    print("     - App ID")
                if not account.app_secret:
                    print("     - App Secret")
            
            print()
        
        # Summary
        configured_accounts = [acc for acc in accounts if acc.is_configured()]
        active_accounts = [acc for acc in accounts if acc.is_active]
        
        print("📈 Summary:")
        print(f"   Total accounts: {len(accounts)}")
        print(f"   Configured: {len(configured_accounts)}")
        print(f"   Active: {len(active_accounts)}")
        
        if len(configured_accounts) > 0:
            print("   ✅ At least one account is ready for use!")
        else:
            print("   ⚠️  No accounts are fully configured")
            print("   📝 Please configure at least one account to use Facebook features")
        
    except Exception as e:
        print(f"❌ Error testing accounts: {str(e)}")
    finally:
        db.close()

def list_account_requirements():
    """List requirements for each account type"""
    
    print("\n📋 Account Configuration Requirements:")
    print("=" * 50)
    
    print("\n🔧 Manual Account Requirements:")
    print("   - App ID and App Secret")
    print("   - Access Token (from Facebook Login)")
    print("   - Page ID (for posting)")
    print("   - User ID (optional)")
    
    print("\n🤖 Auto Account Requirements:")
    print("   - App ID and App Secret")
    print("   - Access Token (from Facebook Login)")
    print("   - Page ID (for posting)")
    print("   - User ID (optional)")
    print("   - Automation configuration (JSON)")
    
    print("\n📝 To configure accounts:")
    print("   1. Run: python configure_auto_account_1_account.py")
    print("   2. Run: python configure_auto_account_2_account.py")
    print("   3. Or use the web interface at: https://autosell-frontend.onrender.com")

if __name__ == "__main__":
    test_facebook_accounts()
    list_account_requirements()
