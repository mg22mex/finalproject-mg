#!/usr/bin/env python3
"""
System Health Check Script for Autosell.mx
Tests all fixes and verifies system functionality
"""

import requests
import time
import sys
import json
from datetime import datetime

def test_backend_health():
    """Test backend health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend Health: OK")
            return True
        else:
            print(f"❌ Backend Health: Failed ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Backend Health: Error - {e}")
        return False

def test_vehicles_endpoint():
    """Test vehicles endpoint for validation errors"""
    try:
        response = requests.get("http://localhost:8000/vehicles/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Vehicles Endpoint: OK ({len(data)} vehicles)")
            return True
        else:
            print(f"❌ Vehicles Endpoint: Failed ({response.status_code})")
            if response.status_code == 500:
                print("   This indicates the Pydantic validation fix may not be working")
            return False
    except Exception as e:
        print(f"❌ Vehicles Endpoint: Error - {e}")
        return False

def test_frontend_endpoints():
    """Test frontend integration endpoints"""
    endpoints = [
        "/frontend/frontend/sync-to-sheets",
        "/frontend/frontend/post-to-facebook", 
        "/frontend/frontend/complete-vehicle-processing",
        "/frontend/frontend/trigger-sheets-sync"
    ]
    
    all_ok = True
    for endpoint in endpoints:
        try:
            response = requests.post(f"http://localhost:8000{endpoint}", 
                                   json={"marca": "Test", "modelo": "Test"}, 
                                   timeout=5)
            if response.status_code in [200, 422]:  # 422 is OK for missing data
                print(f"✅ {endpoint}: OK")
            else:
                print(f"❌ {endpoint}: Failed ({response.status_code})")
                all_ok = False
        except Exception as e:
            print(f"❌ {endpoint}: Error - {e}")
            all_ok = False
    
    return all_ok

def test_n8n_health():
    """Test n8n health"""
    try:
        response = requests.get("http://localhost:5678", timeout=5)
        if response.status_code == 200:
            print("✅ n8n Health: OK")
            return True
        else:
            print(f"❌ n8n Health: Failed ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ n8n Health: Error - {e}")
        return False

def test_frontend_dev_server():
    """Test if frontend dev server is running"""
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend Dev Server: OK")
            return True
        else:
            print(f"❌ Frontend Dev Server: Failed ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Frontend Dev Server: Error - {e}")
        return False

def main():
    """Run all system health checks"""
    print("🏥 Autosell.mx System Health Check")
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Wait a moment for services to start
    print("⏳ Waiting for services to start...")
    time.sleep(3)
    
    # Run all tests
    results = {
        "Backend Health": test_backend_health(),
        "Vehicles Endpoint": test_vehicles_endpoint(),
        "Frontend Endpoints": test_frontend_endpoints(),
        "n8n Health": test_n8n_health(),
        "Frontend Dev Server": test_frontend_dev_server()
    }
    
    print("\n" + "=" * 50)
    print("📊 HEALTH CHECK RESULTS:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print("=" * 50)
    print(f"📈 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All systems are operational!")
        return 0
    else:
        print("⚠️  Some systems need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())
