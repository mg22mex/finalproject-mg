#!/usr/bin/env python3
"""
Update vehicle with Drive folder information
"""

import os
import sys
sys.path.append('.')

from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5434/autosell_db')

def update_vehicle_drive_info(vehicle_id, folder_id, folder_url):
    """Update vehicle with Drive folder information"""
    print(f"🔧 Updating vehicle {vehicle_id} with Drive folder info...")
    
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # Update the vehicle with Drive folder information
            conn.execute(text("""
                UPDATE vehicles 
                SET drive_folder_id = :folder_id, drive_folder_url = :folder_url 
                WHERE id = :vehicle_id
            """), {
                'folder_id': folder_id,
                'folder_url': folder_url,
                'vehicle_id': vehicle_id
            })
            
            conn.commit()
            print(f"✅ Vehicle {vehicle_id} updated with Drive folder info")
            
            # Verify the update
            result = conn.execute(text("""
                SELECT id, marca, modelo, año, drive_folder_id, drive_folder_url
                FROM vehicles 
                WHERE id = :vehicle_id
            """), {'vehicle_id': vehicle_id})
            
            row = result.fetchone()
            if row:
                print(f"📊 Updated vehicle: {row[1]} {row[2]} ({row[3]})")
                print(f"📁 Drive Folder ID: {row[4]}")
                print(f"📁 Drive Folder URL: {row[5]}")
                return True
            else:
                print(f"❌ Vehicle {vehicle_id} not found")
                return False
                
    except Exception as e:
        print(f"❌ Error updating vehicle: {e}")
        return False

if __name__ == "__main__":
    # Update vehicle 42483 with the Drive folder information
    success = update_vehicle_drive_info(
        vehicle_id=42483,
        folder_id='1MfZIeltAKLLro_9LiDkwx8gAeOVHAxd8',
        folder_url='https://drive.google.com/drive/folders/1MfZIeltAKLLro_9LiDkwx8gAeOVHAxd8'
    )
    
    if success:
        print("🎉 Vehicle updated successfully!")
    else:
        print("❌ Failed to update vehicle")
