#!/usr/bin/env python3
"""
Import 131 vehicles from Google Sheets data
This replaces N8N and gives you full control
"""
import requests
import json
import time

# Backend API endpoint
BACKEND_URL = "http://localhost:8001"

# Your 131 vehicles from Google Sheets (rows 101-231)
# This is a sample - you'll need to replace with your actual data
vehicles_data = [
    # Add your actual 131 vehicles here
    # Format: {"marca": "BRAND", "modelo": "MODEL", "año": 2020, "precio": 250000, ...}
]

def import_vehicles():
    print(f"🚗 Importing {len(vehicles_data)} vehicles to {BACKEND_URL}/vehicles/")
    print("=" * 60)
    
    success_count = 0
    error_count = 0
    
    for i, vehicle_data in enumerate(vehicles_data, 1):
        try:
            response = requests.post(f"{BACKEND_URL}/vehicles/", json=vehicle_data, headers={'Content-Type': 'application/json'})
            response.raise_for_status()
            print(f"✅ {i:3d}/131 - {vehicle_data['marca']} {vehicle_data['modelo']} - ${vehicle_data['precio']:,}")
            success_count += 1
        except requests.exceptions.RequestException as e:
            print(f"❌ {i:3d}/131 - {vehicle_data['marca']} {vehicle_data['modelo']} - ERROR: {e}")
            error_count += 1
        
        # Small delay to avoid overwhelming the backend
        time.sleep(0.1)
    
    print("=" * 60)
    print(f"📊 Import Summary:")
    print(f"   ✅ Successfully imported: {success_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   📈 Total vehicles: {success_count}")
    
    # Check final dashboard stats
    try:
        response = requests.get(f"{BACKEND_URL}/dashboard/stats")
        stats = response.json()
        print(f"\n🎯 Dashboard Stats:")
        print(f"   🚗 Total Vehicles: {stats['total_vehicles']}")
        print(f"   💰 Total Value: ${stats['total_value']:,}")
        print(f"   📸 Total Photos: {stats['total_photos']}")
    except Exception as e:
        print(f"❌ Could not fetch dashboard stats: {e}")

if __name__ == "__main__":
    print("⚠️  IMPORTANT: This script needs your actual 131 vehicles data.")
    print("   Please replace the vehicles_data list with your real data from Google Sheets.")
    print("   Then run: python import_131_vehicles.py")
    print()
    
    if len(vehicles_data) == 0:
        print("❌ No vehicles data found. Please add your 131 vehicles to the script.")
    else:
        import_vehicles()
