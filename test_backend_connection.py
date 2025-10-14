#!/usr/bin/env python3
"""
Test script to check backend connection and vehicle data
"""
import requests
import json

def test_backend_connection():
    print("🔍 Testing Backend Connection")
    print("=" * 50)
    
    backend_url = "http://localhost:8001"
    
    # Test health endpoint
    try:
        print("1. Testing health endpoint...")
        response = requests.get(f"{backend_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False
    
    # Test vehicles endpoint
    try:
        print("\n2. Testing vehicles endpoint...")
        response = requests.get(f"{backend_url}/vehicles", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Vehicles endpoint working")
            print(f"   Total vehicles: {data.get('total', 0)}")
            if data.get('vehicles'):
                print("   Sample vehicle:")
                vehicle = data['vehicles'][0]
                print(f"     - ID: {vehicle.get('id')}")
                print(f"     - Marca: {vehicle.get('marca')}")
                print(f"     - Modelo: {vehicle.get('modelo')}")
                print(f"     - Año: {vehicle.get('año')}")
            else:
                print("   ⚠️ No vehicles found in backend")
        else:
            print(f"❌ Vehicles endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Vehicles endpoint error: {e}")
        return False
    
    # Test sync-from-sheets endpoint
    try:
        print("\n3. Testing sync-from-sheets endpoint...")
        test_vehicle = {
            "marca": "Test",
            "modelo": "Vehicle",
            "año": 2024,
            "color": "Blue",
            "precio": 50000,
            "kilometraje": "10000",
            "estatus": "DISPONIBLE",
            "ubicacion": "Test Location",
            "descripcion": "Test vehicle from N8N",
            "external_id": "GS_Test_2024_123456789"
        }
        
        response = requests.post(
            f"{backend_url}/vehicles/sync-from-sheets",
            json=[test_vehicle],
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ Sync-from-sheets endpoint working")
            result = response.json()
            print(f"   Response: {result}")
        else:
            print(f"❌ Sync-from-sheets endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Sync-from-sheets endpoint error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Backend connection test completed")
    return True

if __name__ == "__main__":
    test_backend_connection()
