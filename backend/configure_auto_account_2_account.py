#!/usr/bin/env python3
"""
Configure Facebook Account: Auto Account 2
Generated configuration script
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db
from app.models.facebook_account import FacebookAccount

def configure_auto_account_2_account():
    """Configure Auto Account 2 Facebook account"""
    
    # Database session
    db = next(get_db())
    
    try:
        # Check if account already exists
        existing_account = db.query(FacebookAccount).filter(
            FacebookAccount.name == "Auto Account 2"
        ).first()
        
        if existing_account:
            print(f"Account '{existing_account.name}' already exists. Updating...")
            account = existing_account
        else:
            print(f"Creating new account: Auto Account 2")
            account = FacebookAccount(
                name="Auto Account 2",
                account_type="auto"  # or "manual" for manual account
            )
            db.add(account)
        
        # Update credentials
        account.app_id = "YOUR_APP_ID_HERE"
        account.app_secret = "YOUR_APP_SECRET_HERE"
        account.is_active = True
        
        # Commit changes
        db.commit()
        
        print(f"✅ Auto Account 2 account configured successfully!")
        print(f"   App ID: YOUR_APP_ID_HERE")
        print(f"   App Secret: YOUR_APP...")
        print(f"   Account ID: {account.id}")
        
        return account.id
        
    except Exception as e:
        print(f"❌ Error configuring Auto Account 2: {str(e)}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    account_id = configure_auto_account_2_account()
    if account_id:
        print(f"\n🎉 Auto Account 2 Facebook account configured with ID: {account_id}")
    else:
        print(f"\n❌ Failed to configure Auto Account 2 Facebook account")
