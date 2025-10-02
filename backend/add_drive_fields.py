#!/usr/bin/env python3
"""
Add Google Drive fields to Vehicle model
This script adds the missing drive_folder_id and drive_folder_url fields to the vehicles table.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add backend directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.database import get_db
from app.models.vehicle import Vehicle

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5434/autosell_db")

def add_drive_fields():
    """Add Google Drive fields to the vehicles table"""
    print("🔧 Adding Google Drive fields to vehicles table...")
    
    engine = create_engine(DATABASE_URL)
    
    try:
        with engine.connect() as conn:
            # Check if columns already exist
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'vehicles' 
                AND column_name IN ('drive_folder_id', 'drive_folder_url')
            """))
            existing_columns = [row[0] for row in result.fetchall()]
            
            if 'drive_folder_id' not in existing_columns:
                print("➕ Adding drive_folder_id column...")
                conn.execute(text("ALTER TABLE vehicles ADD COLUMN drive_folder_id VARCHAR(200)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS ix_vehicles_drive_folder_id ON vehicles (drive_folder_id)"))
                print("✅ drive_folder_id column added")
            else:
                print("✅ drive_folder_id column already exists")
            
            if 'drive_folder_url' not in existing_columns:
                print("➕ Adding drive_folder_url column...")
                conn.execute(text("ALTER TABLE vehicles ADD COLUMN drive_folder_url VARCHAR(500)"))
                print("✅ drive_folder_url column added")
            else:
                print("✅ drive_folder_url column already exists")
            
            conn.commit()
            print("🎉 Google Drive fields added successfully!")
            
    except Exception as e:
        print(f"❌ Error adding Drive fields: {e}")
        return False
    
    return True

if __name__ == "__main__":
    add_drive_fields()
