#!/usr/bin/env python3
"""
Test script for the new API structure
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    try:
        print("🧪 Testing imports...")
        
        # Test database
        from app.database import get_db, init_db, check_db_connection
        print("✅ Database module imported")
        
        # Test models
        from app.models import Vehicle, Photo
        print("✅ Models imported")
        
        # Test schemas
        from app.schemas import VehicleCreate, VehicleResponse
        print("✅ Schemas imported")
        
        # Test API
        from app.api import vehicles_router, health_router
        print("✅ API routers imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_schemas():
    """Test Pydantic schemas"""
    try:
        print("\n🧪 Testing schemas...")
        
        from app.schemas.vehicle import VehicleCreate, VehicleStatus
        
        # Test vehicle creation
        vehicle_data = {
            "marca": "Toyota",
            "modelo": "Camry",
            "año": 2020,
            "color": "Blanco",
            "precio": 25000.00,
            "estatus": VehicleStatus.DISPONIBLE
        }
        
        vehicle = VehicleCreate(**vehicle_data)
        print(f"✅ Vehicle schema created: {vehicle.marca} {vehicle.modelo}")
        
        return True
        
    except Exception as e:
        print(f"❌ Schema test failed: {e}")
        return False

def test_models():
    """Test SQLAlchemy models"""
    try:
        print("\n🧪 Testing models...")
        
        from app.models.vehicle import Vehicle, VehicleStatus
        
        # Test vehicle model creation
        vehicle = Vehicle(
            marca="Honda",
            modelo="Civic",
            año=2019,
            color="Negro",
            precio=22000.00,
            estatus=VehicleStatus.DISPONIBLE
        )
        
        print(f"✅ Vehicle model created: {vehicle.display_name}")
        print(f"   Available: {vehicle.is_available}")
        print(f"   Sold: {vehicle.is_sold}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def test_api_structure():
    """Test API structure"""
    try:
        print("\n🧪 Testing API structure...")
        
        from app.api.vehicles import router as vehicles_router
        from app.api.health import router as health_router
        
        print(f"✅ Vehicles router: {len(vehicles_router.routes)} routes")
        print(f"✅ Health router: {len(health_router.routes)} routes")
        
        # List available routes
        print("\n📋 Available vehicle routes:")
        for route in vehicles_router.routes:
            print(f"   {route.methods} {route.path}")
        
        return True
        
    except Exception as e:
        print(f"❌ API structure test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚗 Testing Autosell.mx API Structure...")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Schemas", test_schemas),
        ("Models", test_models),
        ("API Structure", test_api_structure),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
            print(f"✅ {test_name} test passed")
        else:
            print(f"❌ {test_name} test failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API structure is ready.")
        print("\n🚀 Next steps:")
        print("   1. Start the database: npm run db:setup")
        print("   2. Run the API: python main.py")
        print("   3. Visit: http://localhost:8000/docs")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
