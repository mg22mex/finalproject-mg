#!/usr/bin/env python3
"""
Database Initialization Script
Sets up the PostgreSQL database with our schema
"""

import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import time

# Database configuration
DB_HOST = "localhost"
DB_PORT = 5433
DB_USER = "autosell_user"
DB_PASSWORD = "autosell_password"
DB_NAME = "autosell_mx"

def wait_for_database():
    """Wait for database to be ready"""
    print("⏳ Waiting for database to be ready...")
    
    for attempt in range(30):  # Wait up to 30 seconds
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                user="postgres",
                password="autosell_password"
            )
            conn.close()
            print("✅ Database is ready!")
            return True
        except psycopg2.OperationalError:
            print(f"⏳ Attempt {attempt + 1}/30: Database not ready yet...")
            time.sleep(1)
    
    print("❌ Database failed to start within 30 seconds")
    return False

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user="postgres",
            password="autosell_password"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        exists = cursor.fetchone()
        
        if not exists:
            print(f"🗄️ Creating database '{DB_NAME}'...")
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"✅ Database '{DB_NAME}' created successfully")
        else:
            print(f"✅ Database '{DB_NAME}' already exists")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to create database: {e}")
        return False

def create_user():
    """Create the application user if it doesn't exist"""
    try:
        # Connect to our database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user="postgres",
            password="autosell_password",
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT 1 FROM pg_user WHERE usename = %s", (DB_USER,))
        exists = cursor.fetchone()
        
        if not exists:
            print(f"👤 Creating user '{DB_USER}'...")
            cursor.execute(f"CREATE USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}'")
            print(f"✅ User '{DB_USER}' created successfully")
        else:
            print(f"✅ User '{DB_USER}' already exists")
        
        # Grant privileges
        print(f"🔐 Granting privileges to '{DB_USER}'...")
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER}")
        cursor.execute(f"GRANT ALL PRIVILEGES ON SCHEMA public TO {DB_USER}")
        cursor.execute(f"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {DB_USER}")
        cursor.execute(f"GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO {DB_USER}")
        print(f"✅ Privileges granted to '{DB_USER}'")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to create user: {e}")
        return False

def run_schema_script():
    """Run the database schema script"""
    try:
        # Connect as our application user
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        # Read and execute the schema script
        schema_file = os.path.join(os.path.dirname(__file__), "init.sql")
        
        if os.path.exists(schema_file):
            print(f"📜 Running schema script: {schema_file}")
            with open(schema_file, 'r') as f:
                schema_sql = f.read()
            
            # Split by semicolon and execute each statement
            statements = schema_sql.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement and not statement.startswith('--'):
                    try:
                        cursor.execute(statement)
                    except Exception as e:
                        print(f"⚠️  Warning executing statement: {e}")
                        print(f"   Statement: {statement[:100]}...")
            
            conn.commit()
            print("✅ Schema script executed successfully")
        else:
            print(f"⚠️  Schema file not found: {schema_file}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to run schema script: {e}")
        return False

def test_connection():
    """Test the database connection"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        # Test basic operations
        cursor.execute("SELECT version()")
        version = cursor.fetchone()
        print(f"✅ Database connection test successful")
        print(f"   PostgreSQL version: {version[0]}")
        
        # Check if our tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("⚠️  No tables found in database")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

def main():
    """Main initialization function"""
    print("🚗 Autosell.mx - Database Initialization")
    print("=" * 50)
    
    # Wait for database to be ready
    if not wait_for_database():
        return False
    
    # Create database
    if not create_database():
        return False
    
    # Create user
    if not create_user():
        return False
    
    # Run schema script
    if not run_schema_script():
        return False
    
    # Test connection
    if not test_connection():
        return False
    
    print("\n🎉 Database initialization completed successfully!")
    print(f"📊 Database: {DB_NAME}")
    print(f"👤 User: {DB_USER}")
    print(f"🔌 Host: {DB_HOST}:{DB_PORT}")
    print(f"🔑 Password: {DB_PASSWORD}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
