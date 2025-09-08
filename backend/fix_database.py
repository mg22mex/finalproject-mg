#!/usr/bin/env python3
"""
Fix Database User Issue
Creates the missing user and tests the connection
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database configuration
DB_HOST = "localhost"
DB_PORT = 5433
DB_NAME = "autosell_mx"

def create_user():
    """Create the autosell_user"""
    try:
        # Connect to postgres database as superuser
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user="autosell_user",
            password="autosell_password",
            database="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create user
        print("👤 Creating autosell_user...")
        cursor.execute("CREATE USER autosell_user WITH PASSWORD 'autosell_password'")
        print("✅ User created successfully")
        
        # Grant privileges
        print("🔐 Granting privileges...")
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO autosell_user")
        cursor.execute(f"GRANT ALL PRIVILEGES ON SCHEMA public TO autosell_user")
        cursor.execute(f"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO autosell_user")
        cursor.execute(f"GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO autosell_user")
        cursor.execute(f"GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO autosell_user")
        print("✅ Privileges granted")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to create user: {e}")
        return False

def test_connection():
    """Test connection as autosell_user"""
    try:
        print("🔌 Testing connection as autosell_user...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user="autosell_user",
            password="autosell_password",
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
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Fixing Database User Issue...")
    print("=" * 40)
    
    if create_user():
        if test_connection():
            print("\n🎉 Database is now working correctly!")
            print("🚀 You can now start the API with: python main.py")
            return True
    
    return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
