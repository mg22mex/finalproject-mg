#!/usr/bin/env python3
"""
Test Database Connection
Tests the connection to the autosell_mx database
"""

import psycopg2

# Database configuration
DB_HOST = "localhost"
DB_PORT = 5433
DB_USER = "autosell_user"
DB_PASSWORD = "autosell_password"
DB_NAME = "autosell_mx"

def test_connection():
    """Test connection to autosell_mx database"""
    try:
        print("🔌 Testing connection to autosell_mx database...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        # Test basic query
        cursor.execute("SELECT COUNT(*) FROM vehicles")
        count = cursor.fetchone()
        print(f"✅ Connection successful! Found {count[0]} vehicles")
        
        # Check tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        print(f"📊 Database has {len(tables)} tables:")
        for table in tables:
            print(f"   - {table[0]}")
        
        # Check if we can insert a test vehicle
        print("\n🧪 Testing vehicle creation...")
        cursor.execute("""
            INSERT INTO vehicles (marca, modelo, año, color, precio, estatus, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, ("Toyota", "Camry", 2020, "Blanco", 25000.00, "Disponible", "test"))
        
        vehicle_id = cursor.fetchone()[0]
        print(f"✅ Test vehicle created with ID: {vehicle_id}")
        
        # Clean up test data
        cursor.execute("DELETE FROM vehicles WHERE id = %s", (vehicle_id,))
        print("🧹 Test vehicle cleaned up")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n🎉 Database connection test successful!")
        print("🚀 The database is ready for the API!")
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
