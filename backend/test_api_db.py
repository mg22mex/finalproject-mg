#!/usr/bin/env python3
"""
Test API Database Connection
Tests the database connection using the same configuration as the API
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_api_database():
    """Test database connection using API configuration"""
    try:
        print("🔌 Testing API database connection...")
        
        # Import the database module
        from app.database import check_db_connection, get_db_stats
        
        print(f"📊 Database URL: {os.getenv('DATABASE_URL', 'Not set')}")
        
        # Test connection
        if check_db_connection():
            print("✅ Database connection successful!")
            
            # Get stats
            stats = get_db_stats()
            print(f"📊 Database stats: {len(stats)} tables")
            
            return True
        else:
            print("❌ Database connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_api_database()
