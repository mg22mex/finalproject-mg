#!/usr/bin/env python3
"""
Simple test to isolate import issues
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_vehicle_only():
    """Test just the Vehicle model without relationships"""
    try:
        print("🧪 Testing Vehicle model only...")
        
        # Import just the Vehicle model
        from app.models.vehicle import Vehicle, VehicleStatus
        
        # Create a simple vehicle
        vehicle = Vehicle(
            marca="Test",
            modelo="Car",
            año=2020
        )
        
        print(f"✅ Vehicle model created: {vehicle.display_name}")
        return True
        
    except Exception as e:
        print(f"❌ Vehicle model test failed: {e}")
        return False

def test_models_individually():
    """Test each model individually"""
    try:
        print("\n🧪 Testing models individually...")
        
        # Test each model
        from app.models.vehicle import Vehicle
        print("✅ Vehicle imported")
        
        from app.models.photo import Photo
        print("✅ Photo imported")
        
        from app.models.status_history import StatusHistory
        print("✅ StatusHistory imported")
        
        return True
        
    except Exception as e:
        print(f"❌ Individual model test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚗 Testing Models Individually...")
    print("=" * 40)
    
    test_vehicle_only()
    test_models_individually()
