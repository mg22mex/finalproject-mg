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

def configure_manual_account_2():
    """Configure Manual Account 2 Facebook account"""
    
    # Database session
    db = next(get_db())
    
    try:
        # Check if account already exists
        existing_account = db.query(FacebookAccount).filter(
            FacebookAccount.name == "Manual Account 2"
        ).first()
        
        if existing_account:
            print(f"Account '{existing_account.name}' already exists. Updating...")
            account = existing_account
        else:
            print(f"Creating new account: Manual Account 2")
            account = FacebookAccount(
                name="Manual Account 2",
                account_type="manual"  # Changed to manual account
            )
            db.add(account)
        
        # Update credentials
        account.app_id = "761619893338419"
        account.app_secret = "34f32c08c5bb4751da6533e96247284c"
        account.is_active = True
        
        # Commit changes
        db.commit()
        
        print(f"✅ Manual Account 2 account configured successfully!")
        print(f"   App ID: {account.app_id}")
        print(f"   App Secret: {account.app_secret[:8]}...")
        print(f"   Account ID: {account.id}")
        
        return account.id
        
    except Exception as e:
        print(f"❌ Error configuring Manual Account 2: {str(e)}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    account_id = configure_manual_account_2()
    if account_id:
        print(f"\n🎉 Manual Account 2 Facebook account configured with ID: {account_id}")
    else:
        print(f"\n❌ Failed to configure Manual Account 2 Facebook account")
