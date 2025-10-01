#!/usr/bin/env python3
"""
Database Cleaning Script for Autosell.mx
Fixes empty and whitespace-only fields in the database
"""

import os
import sys
from sqlalchemy import create_engine, text
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_database():
    """Clean database by fixing empty and whitespace-only fields"""
    
    # Database connection
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/autosell")
    
    try:
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            logger.info("🔧 Starting database cleanup...")
            
            # Start transaction
            trans = conn.begin()
            
            try:
                # Fix empty marca fields
                result1 = conn.execute(text("""
                    UPDATE vehicles 
                    SET marca = 'Unknown' 
                    WHERE marca IS NULL OR TRIM(marca) = ''
                """))
                logger.info(f"✅ Fixed {result1.rowcount} empty marca fields")
                
                # Fix empty modelo fields
                result2 = conn.execute(text("""
                    UPDATE vehicles 
                    SET modelo = 'Unknown' 
                    WHERE modelo IS NULL OR TRIM(modelo) = ''
                """))
                logger.info(f"✅ Fixed {result2.rowcount} empty modelo fields")
                
                # Fix empty color fields
                result3 = conn.execute(text("""
                    UPDATE vehicles 
                    SET color = 'Unknown' 
                    WHERE color IS NULL OR TRIM(color) = ''
                """))
                logger.info(f"✅ Fixed {result3.rowcount} empty color fields")
                
                # Fix empty ubicacion fields
                result4 = conn.execute(text("""
                    UPDATE vehicles 
                    SET ubicacion = 'Unknown' 
                    WHERE ubicacion IS NULL OR TRIM(ubicacion) = ''
                """))
                logger.info(f"✅ Fixed {result4.rowcount} empty ubicacion fields")
                
                # Commit transaction
                trans.commit()
                logger.info("✅ Database cleanup completed successfully!")
                
                # Verify results
                result = conn.execute(text("SELECT COUNT(*) FROM vehicles WHERE marca = 'Unknown' OR modelo = 'Unknown'"))
                count = result.scalar()
                logger.info(f"📊 Total vehicles with 'Unknown' fields: {count}")
                
            except Exception as e:
                trans.rollback()
                logger.error(f"❌ Error during cleanup: {e}")
                raise
                
    except Exception as e:
        logger.error(f"❌ Database connection error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    clean_database()
