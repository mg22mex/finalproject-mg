#!/usr/bin/env python3
"""
Test Drive Service directly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.drive_service import GoogleDriveService

def test_drive_service():
    """Test Drive service directly"""
    print("🔧 Testing Drive Service Directly")
    print("=" * 40)
    
    try:
        # Initialize Drive service
        drive_service = GoogleDriveService()
        
        # Test authentication
        print("🔄 Testing authentication...")
        if drive_service.authenticate():
            print("✅ Authentication successful")
        else:
            print("❌ Authentication failed")
            return False
        
        # Test folder creation
        print("🔄 Testing folder creation...")
        vehicle_info = {
            'marca': 'Test',
            'modelo': 'Vehicle',
            'año': 2024
        }
        folder_info = drive_service.create_vehicle_folder(999, vehicle_info)
        if folder_info:
            print(f"✅ Folder created: {folder_info['folder_name']} (ID: {folder_info['folder_id']})")
            print(f"🔗 Folder URL: {folder_info['folder_url']}")
        else:
            print("❌ Folder creation failed")
            return False
        
        print("\n🎉 All Drive service tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing Drive service: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_drive_service()
