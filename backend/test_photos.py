#!/usr/bin/env python3
"""
Test photos endpoint directly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db
from app.models.photo import Photo

def test_photos():
    """Test photos database directly"""
    print("🔍 Testing Photos Database")
    print("=" * 40)
    
    try:
        db = next(get_db())
        photos = db.query(Photo).all()
        
        print(f"✅ Found {len(photos)} photos in database")
        
        if photos:
            for photo in photos[:3]:  # Show first 3 photos
                print(f"📸 Photo ID: {photo.id}, Vehicle: {photo.vehicle_id}, File: {photo.filename}")
        else:
            print("📷 No photos found in database")
            print("💡 This explains why you don't see photos in the frontend")
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing photos: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_photos()
