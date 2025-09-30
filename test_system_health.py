#!/usr/bin/env python3
"""
Complete System Health Check for Autosell.mx
Tests all components and integrations
"""

import requests
import json
import sys
import time
from datetime import datetime

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def print_info(message):
    """Print info message"""
    print(f"ℹ️  {message}")

def test_backend_health():
    """Test backend health and basic functionality"""
    print_header("Testing Backend Health")
    
    try:
        # Test health endpoint
        response = requests.get("http://127.0.0.1:8000/health", timeout=5)
        if response.status_code == 200:
            print_success("Backend health check passed")
        else:
            print_error(f"Backend health check failed: {response.status_code}")
            return False
        
        # Test root endpoint
        response = requests.get("http://127.0.0.1:8000/", timeout=5)
        if response.status_code == 200:
            print_success("Backend root endpoint accessible")
        else:
            print_error(f"Backend root endpoint failed: {response.status_code}")
            return False
        
        # Test vehicles endpoint
        response = requests.get("http://127.0.0.1:8000/vehicles/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Vehicles endpoint working - {len(data.get('vehicles', []))} vehicles")
        else:
            print_error(f"Vehicles endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Backend connection failed: {e}")
        return False

def test_n8n_health():
    """Test n8n health and accessibility"""
    print_header("Testing n8n Health")
    
    try:
        # Test n8n dashboard
        response = requests.get("http://127.0.0.1:5678/", timeout=5)
        if response.status_code == 200:
            print_success("n8n dashboard accessible")
        else:
            print_error(f"n8n dashboard failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"n8n connection failed: {e}")
        return False

def test_frontend_endpoints():
    """Test frontend integration endpoints"""
    print_header("Testing Frontend Integration Endpoints")
    
    try:
        # Test sync to sheets endpoint
        test_data = {
            "marca": "Toyota",
            "modelo": "Camry",
            "año": 2020,
            "color": "Blanco",
            "precio": 250000,
            "kilometraje": "45,000 km",
            "estatus": "DISPONIBLE",
            "ubicacion": "CDMX"
        }
        
        response = requests.post(
            "http://127.0.0.1:8000/frontend/frontend/sync-to-sheets",
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print_success("Frontend sync to sheets endpoint working")
        else:
            print_error(f"Frontend sync to sheets failed: {response.status_code} - {response.text}")
            return False
        
        # Test Facebook posting endpoint
        response = requests.post(
            "http://127.0.0.1:8000/frontend/frontend/post-to-facebook",
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print_success("Frontend Facebook posting endpoint working")
        else:
            print_error(f"Frontend Facebook posting failed: {response.status_code} - {response.text}")
            return False
        
        # Test complete processing endpoint
        response = requests.post(
            "http://127.0.0.1:8000/frontend/frontend/complete-vehicle-processing",
            json=test_data,
            timeout=15
        )
        
        if response.status_code == 200:
            print_success("Frontend complete processing endpoint working")
        else:
            print_error(f"Frontend complete processing failed: {response.status_code} - {response.text}")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Frontend endpoints error: {e}")
        return False

def test_google_sheets_sync():
    """Test Google Sheets sync functionality"""
    print_header("Testing Google Sheets Sync")
    
    try:
        # Test sync trigger
        response = requests.post(
            "http://127.0.0.1:8000/frontend/frontend/trigger-sheets-sync",
            json={},
            timeout=10
        )
        
        if response.status_code == 200:
            print_success("Google Sheets sync trigger working")
        else:
            print_error(f"Google Sheets sync trigger failed: {response.status_code} - {response.text}")
            return False
        
        # Test direct sync endpoint
        test_vehicles = [
            {
                "external_id": "GS_TEST_001",
                "marca": "Toyota",
                "modelo": "Camry",
                "año": 2020,
                "color": "Blanco",
                "precio": 250000,
                "kilometraje": "45,000 km",
                "estatus": "DISPONIBLE",
                "ubicacion": "CDMX",
                "descripcion": "Toyota Camry 2020"
            }
        ]
        
        response = requests.post(
            "http://127.0.0.1:8000/vehicles/sync-from-sheets",
            json=test_vehicles,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Direct sync endpoint working - {data.get('synced_count', 0)} vehicles synced")
        else:
            print_error(f"Direct sync endpoint failed: {response.status_code} - {response.text}")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Google Sheets sync error: {e}")
        return False

def test_vehicle_removal():
    """Test vehicle removal functionality"""
    print_header("Testing Vehicle Removal")
    
    try:
        # First, get a real vehicle ID
        vehicles_response = requests.get("http://127.0.0.1:8000/vehicles/", timeout=5)
        if vehicles_response.status_code != 200:
            print_error("Could not fetch vehicles to get valid ID")
            return False
        
        vehicles_data = vehicles_response.json()
        vehicles = vehicles_data.get('vehicles', [])
        if not vehicles:
            print_error("No vehicles found in database")
            return False
        
        # Use the first vehicle's ID
        vehicle_id = vehicles[0]['id']
        print(f"Testing with vehicle ID: {vehicle_id}")
        
        # Test Autosell removal
        response = requests.post(
            f"http://127.0.0.1:8000/vehicles/{vehicle_id}/remove-from-autosell",
            timeout=5
        )
        
        if response.status_code == 200:
            print_success("Autosell removal endpoint working")
        else:
            print_error(f"Autosell removal failed: {response.status_code} - {response.text}")
            return False
        
        # Test Facebook removal
        response = requests.post(
            f"http://127.0.0.1:8000/vehicles/{vehicle_id}/remove-from-facebook",
            timeout=5
        )
        
        if response.status_code == 200:
            print_success("Facebook removal endpoint working")
        else:
            print_error(f"Facebook removal failed: {response.status_code} - {response.text}")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Vehicle removal error: {e}")
        return False

def test_database_connectivity():
    """Test database connectivity and data integrity"""
    print_header("Testing Database Connectivity")
    
    try:
        # Test vehicles endpoint to check database
        response = requests.get("http://127.0.0.1:8000/vehicles/", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            vehicles = data.get('vehicles', [])
            print_success(f"Database connected - {len(vehicles)} vehicles found")
            
            # Check for different statuses
            statuses = {}
            for vehicle in vehicles:
                status = vehicle.get('estatus', 'UNKNOWN')
                statuses[status] = statuses.get(status, 0) + 1
            
            print_info(f"Vehicle statuses: {statuses}")
            
            return True
        else:
            print_error(f"Database connectivity failed: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Database connectivity error: {e}")
        return False

def test_api_documentation():
    """Test API documentation accessibility"""
    print_header("Testing API Documentation")
    
    try:
        # Test OpenAPI docs
        response = requests.get("http://127.0.0.1:8000/docs", timeout=5)
        if response.status_code == 200:
            print_success("API documentation accessible")
        else:
            print_error(f"API documentation failed: {response.status_code}")
            return False
        
        # Test OpenAPI schema
        response = requests.get("http://127.0.0.1:8000/openapi.json", timeout=5)
        if response.status_code == 200:
            print_success("OpenAPI schema accessible")
        else:
            print_error(f"OpenAPI schema failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"API documentation error: {e}")
        return False

def run_performance_test():
    """Run basic performance tests"""
    print_header("Running Performance Tests")
    
    try:
        # Test response times
        start_time = time.time()
        response = requests.get("http://127.0.0.1:8000/vehicles/", timeout=5)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        if response.status_code == 200:
            print_success(f"Vehicles endpoint response time: {response_time:.2f}ms")
            
            if response_time < 1000:  # Less than 1 second
                print_success("Performance: Good")
            elif response_time < 3000:  # Less than 3 seconds
                print_info("Performance: Acceptable")
            else:
                print_error("Performance: Slow")
        else:
            print_error(f"Performance test failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Performance test error: {e}")
        return False

def generate_report(results):
    """Generate a comprehensive test report"""
    print_header("Test Report")
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    failed_tests = total_tests - passed_tests
    
    print(f"📊 Test Results: {passed_tests}/{total_tests} tests passed")
    print(f"✅ Passed: {passed_tests}")
    print(f"❌ Failed: {failed_tests}")
    
    if failed_tests > 0:
        print("\n❌ Failed Tests:")
        for test_name, result in results.items():
            if not result:
                print(f"  - {test_name}")
    
    print(f"\n🕐 Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! Your Autosell.mx system is healthy!")
        print("\n📋 Next Steps:")
        print("1. Configure n8n workflows")
        print("2. Set up Google Sheets credentials")
        print("3. Configure Facebook credentials")
        print("4. Test complete automation pipeline")
    else:
        print(f"\n⚠️  {failed_tests} tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("1. Check if all services are running")
        print("2. Verify port numbers and URLs")
        print("3. Check logs for error messages")
        print("4. Ensure all dependencies are installed")

def main():
    """Run all system health checks"""
    print("🏥 Autosell.mx System Health Check")
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all tests
    results = {
        "Backend Health": test_backend_health(),
        "n8n Health": test_n8n_health(),
        "Frontend Endpoints": test_frontend_endpoints(),
        "Google Sheets Sync": test_google_sheets_sync(),
        "Vehicle Removal": test_vehicle_removal(),
        "Database Connectivity": test_database_connectivity(),
        "API Documentation": test_api_documentation(),
        "Performance": run_performance_test()
    }
    
    # Generate report
    generate_report(results)
    
    # Exit with appropriate code
    if all(results.values()):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
