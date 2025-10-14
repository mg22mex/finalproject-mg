#!/usr/bin/env python3
"""
Test script to manually add a vehicle and test the frontend
"""
import requests
import json

def test_manual_vehicle():
    print("🚗 Testing Manual Vehicle Creation")
    print("=" * 50)
    
    backend_url = "http://localhost:8001"
    
    # Test vehicle data
    test_vehicle = {
        "marca": "Toyota",
        "modelo": "Corolla",
        "año": 2022,
        "color": "Blanco",
        "precio": 250000,
        "kilometraje": "50000",
        "estatus": "DISPONIBLE",
        "ubicacion": "Ciudad de México",
        "descripcion": "Toyota Corolla 2022 en excelente estado",
        "external_id": "MANUAL_TEST_001"
    }
    
    try:
        print("1. Creating test vehicle...")
        response = requests.post(
            f"{backend_url}/vehicles",
            json=test_vehicle,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Vehicle created successfully!")
            print(f"   Vehicle ID: {result.get('id')}")
            print(f"   Marca: {result.get('marca')}")
            print(f"   Modelo: {result.get('modelo')}")
        else:
            print(f"❌ Vehicle creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error creating vehicle: {e}")
        return False
    
    # Test getting vehicles
    try:
        print("\n2. Testing vehicle retrieval...")
        response = requests.get(f"{backend_url}/vehicles", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Vehicles retrieved successfully!")
            print(f"   Total vehicles: {data.get('total', 0)}")
            
            if data.get('vehicles'):
                print("   Vehicles found:")
                for vehicle in data['vehicles']:
                    print(f"     - ID: {vehicle.get('id')}, {vehicle.get('marca')} {vehicle.get('modelo')} ({vehicle.get('año')})")
            else:
                print("   ⚠️ No vehicles found")
        else:
            print(f"❌ Vehicle retrieval failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error retrieving vehicles: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ Manual vehicle test completed")
    print("🌐 Now check your frontend at http://localhost:3002")
    return True

if __name__ == "__main__":
    test_manual_vehicle()
