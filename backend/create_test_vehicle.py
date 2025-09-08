#!/usr/bin/env python3
"""
Create Test Vehicle
Adds a test vehicle to the database for testing the photo system
"""

import psycopg2
from datetime import datetime

# Database configuration
DB_HOST = "localhost"
DB_PORT = 5433
DB_USER = "autosell_user"
DB_PASSWORD = "autosell_password"
DB_NAME = "autosell_mx"

def create_test_vehicle():
    """Create a test vehicle in the database"""
    try:
        print("🔌 Connecting to database...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()

        # Create test vehicle
        print("🚗 Creating test vehicle...")
        cursor.execute("""
            INSERT INTO vehicles (marca, modelo, año, color, precio, estatus, ubicacion, descripcion, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, ("Toyota", "Camry", 2020, "Blanco", 25000.00, "Disponible", "Ciudad de México", "Excelente estado, bajo kilometraje", "test"))

        vehicle_id = cursor.fetchone()[0]
        print(f"✅ Test vehicle created with ID: {vehicle_id}")

        # Create another test vehicle
        cursor.execute("""
            INSERT INTO vehicles (marca, modelo, año, color, precio, estatus, ubicacion, descripcion, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, ("Honda", "Civic", 2019, "Negro", 22000.00, "Disponible", "Guadalajara", "Bien conservado, revisión completa", "test"))

        vehicle_id_2 = cursor.fetchone()[0]
        print(f"✅ Second test vehicle created with ID: {vehicle_id_2}")

        # Create a third test vehicle
        cursor.execute("""
            INSERT INTO vehicles (marca, modelo, año, color, precio, estatus, ubicacion, descripcion, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, ("Nissan", "Sentra", 2021, "Azul", 28000.00, "FOTOS", "Monterrey", "Nuevo modelo, fotos en proceso", "test"))

        vehicle_id_3 = cursor.fetchone()[0]
        print(f"✅ Third test vehicle created with ID: {vehicle_id_3}")

        conn.commit()
        cursor.close()
        conn.close()

        print("\n🎉 Test vehicles created successfully!")
        print(f"   - Toyota Camry 2020 (ID: {vehicle_id})")
        print(f"   - Honda Civic 2019 (ID: {vehicle_id_2})")
        print(f"   - Nissan Sentra 2021 (ID: {vehicle_id_3})")
        print("\n🚀 You can now test the photo management system!")
        return True

    except Exception as e:
        print(f"❌ Failed to create test vehicle: {e}")
        return False

if __name__ == "__main__":
    create_test_vehicle()
