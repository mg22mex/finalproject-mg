#!/usr/bin/env python3
"""
Import vehicles from Google Sheets to the backend
"""
import requests
import json
import time

# Backend API endpoint
BACKEND_URL = "http://localhost:8001"

# Sample vehicle data (you can replace this with actual Google Sheets data)
sample_vehicles = [
    {
        "marca": "MAZDA",
        "modelo": "CX30",
        "año": 2021,
        "precio": 379000,
        "estatus": "DISPONIBLE",
        "color": "BLANCA",
        "kilometraje": "",
        "ubicacion": "PERIFERICO",
        "descripcion": "MAZDA CX30 2021"
    },
    {
        "marca": "CHEVROLET",
        "modelo": "AVEO LT STD",
        "año": 2018,
        "precio": 191000,
        "estatus": "DISPONIBLE",
        "color": "PLATA",
        "kilometraje": "73618",
        "ubicacion": "PERIFERICO",
        "descripcion": "CHEVROLET AVEO LT STD 2018"
    },
    {
        "marca": "MAZDA",
        "modelo": "MAZDA 3 IGT",
        "año": 2019,
        "precio": 309000,
        "estatus": "DISPONIBLE",
        "color": "GRIS",
        "kilometraje": "74000",
        "ubicacion": "PERIFERICO",
        "descripcion": "MAZDA MAZDA 3 IGT 2019"
    },
    {
        "marca": "BMW",
        "modelo": "220I",
        "año": 2016,
        "precio": 290000,
        "estatus": "DISPONIBLE",
        "color": "GRIS",
        "kilometraje": "85000",
        "ubicacion": "PERIFERICO",
        "descripcion": "BMW 220I 2016"
    },
    {
        "marca": "NISSAN",
        "modelo": "NP300 REG CAB",
        "año": 2021,
        "precio": 339000,
        "estatus": "DISPONIBLE",
        "color": "PLATA",
        "kilometraje": "15000",
        "ubicacion": "PERIFERICO",
        "descripcion": "NISSAN NP300 REG CAB 2021"
    },
    {
        "marca": "BUICK",
        "modelo": "ENVISION AVENIR",
        "año": 2021,
        "precio": 585000,
        "estatus": "DISPONIBLE",
        "color": "ROJO",
        "kilometraje": "12000",
        "ubicacion": "PERIFERICO",
        "descripcion": "BUICK ENVISION AVENIR 2021"
    }
]

def import_vehicles():
    """Import vehicles to the backend"""
    print("🚀 Starting vehicle import...")
    
    # Check if backend is running
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        if response.status_code != 200:
            print("❌ Backend is not running")
            return False
    except:
        print("❌ Backend is not running")
        return False
    
    print("✅ Backend is running")
    
    # Import each vehicle
    imported_count = 0
    for i, vehicle in enumerate(sample_vehicles):
        try:
            response = requests.post(f"{BACKEND_URL}/vehicles", json=vehicle)
            if response.status_code == 200:
                imported_count += 1
                print(f"✅ Imported vehicle {i+1}: {vehicle['marca']} {vehicle['modelo']}")
            else:
                print(f"❌ Failed to import vehicle {i+1}: {response.text}")
        except Exception as e:
            print(f"❌ Error importing vehicle {i+1}: {e}")
        
        # Small delay to avoid overwhelming the backend
        time.sleep(0.1)
    
    print(f"🎯 Imported {imported_count} vehicles successfully")
    
    # Check final stats
    try:
        response = requests.get(f"{BACKEND_URL}/dashboard/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"📊 Final stats: {stats['total_vehicles']} vehicles, ${stats['total_value']:,.2f} total value")
        else:
            print("❌ Could not get final stats")
    except Exception as e:
        print(f"❌ Error getting final stats: {e}")
    
    return True

if __name__ == "__main__":
    import_vehicles()
