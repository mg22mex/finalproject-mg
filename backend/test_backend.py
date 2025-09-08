#!/usr/bin/env python3
"""
Simple test script to verify backend functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required packages can be imported"""
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
        
        import uvicorn
        print("✅ Uvicorn imported successfully")
        
        import sqlalchemy
        print("✅ SQLAlchemy imported successfully")
        
        import redis
        print("✅ Redis imported successfully")
        
        import google.auth
        print("✅ Google Auth imported successfully")
        
        import facebook_business
        print("✅ Facebook Business imported successfully")
        
        import tweepy
        print("✅ Tweepy imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_fastapi_app():
    """Test that we can create a FastAPI app"""
    try:
        from main import app
        print("✅ FastAPI app created successfully")
        print(f"   App title: {app.title}")
        print(f"   App version: {app.version}")
        return True
    except Exception as e:
        print(f"❌ FastAPI app creation failed: {e}")
        return False

def test_environment():
    """Test environment variables"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check if we can access environment variables
        debug = os.getenv("DEBUG", "false")
        print(f"✅ Environment loaded successfully (DEBUG: {debug})")
        return True
    except Exception as e:
        print(f"❌ Environment loading failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚗 Testing Autosell.mx Backend...")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("FastAPI App", test_fastapi_app),
        ("Environment", test_environment),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing: {test_name}")
        if test_func():
            passed += 1
            print(f"✅ {test_name} passed")
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready to run.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
