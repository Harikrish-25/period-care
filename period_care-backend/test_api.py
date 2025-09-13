#!/usr/bin/env python3
"""
Test script to verify Period Care Backend functionality
"""

import requests
import json
from datetime import date, timedelta


BASE_URL = "http://localhost:8000"
admin_token = None
user_token = None


def test_health_check():
    """Test basic health check"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False


def test_admin_login():
    """Test admin login"""
    global admin_token
    print("🔐 Testing admin login...")
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
            "email": "admin@periodcare.com",
            "password": "admin123"
        })
        if response.status_code == 200:
            data = response.json()
            admin_token = data["access_token"]
            print("✅ Admin login successful")
            return True
        else:
            print(f"❌ Admin login failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Admin login error: {e}")
        return False


def test_user_login():
    """Test user login"""
    global user_token
    print("👤 Testing user login...")
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
            "email": "priya@example.com",
            "password": "user123"
        })
        if response.status_code == 200:
            data = response.json()
            user_token = data["access_token"]
            print("✅ User login successful")
            return True
        else:
            print(f"❌ User login failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ User login error: {e}")
        return False


def test_get_kits():
    """Test getting kits"""
    print("📦 Testing get kits...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/kits/")
        if response.status_code == 200:
            kits = response.json()
            print(f"✅ Found {len(kits)} kits")
            return True
        else:
            print(f"❌ Get kits failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get kits error: {e}")
        return False


def test_get_fruits():
    """Test getting fruits"""
    print("🍎 Testing get fruits...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/fruits/")
        if response.status_code == 200:
            fruits = response.json()
            print(f"✅ Found {len(fruits)} fruits")
            return True
        else:
            print(f"❌ Get fruits failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get fruits error: {e}")
        return False


def test_get_nutrients():
    """Test getting nutrients"""
    print("💊 Testing get nutrients...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/nutrients/")
        if response.status_code == 200:
            nutrients = response.json()
            print(f"✅ Found {len(nutrients)} nutrients")
            return True
        else:
            print(f"❌ Get nutrients failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get nutrients error: {e}")
        return False


def test_create_order():
    """Test creating an order"""
    print("🛒 Testing create order...")
    if not user_token:
        print("❌ User token not available")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {user_token}"}
        order_data = {
            "kit_id": 1,
            "selected_fruits": json.dumps([1, 2]),
            "selected_nutrients": json.dumps([1]),
            "scheduled_date": (date.today() + timedelta(days=7)).isoformat(),
            "delivery_address": "123 Test Street, Mumbai, Maharashtra 400001"
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/orders/", 
                               json=order_data, headers=headers)
        if response.status_code == 200:
            order = response.json()
            print(f"✅ Order created successfully: ID {order['id']}")
            return True
        else:
            print(f"❌ Create order failed: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ Create order error: {e}")
        return False


def test_admin_dashboard():
    """Test admin dashboard"""
    print("📊 Testing admin dashboard...")
    if not admin_token:
        print("❌ Admin token not available")
        return False
    
    try:
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(f"{BASE_URL}/api/v1/admin/dashboard/stats", 
                              headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print("✅ Admin dashboard accessible")
            print(f"   • Total users: {stats['users']['total']}")
            print(f"   • Total orders: {stats['orders']['total']}")
            return True
        else:
            print(f"❌ Admin dashboard failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Admin dashboard error: {e}")
        return False


def test_benefits_and_testimonials():
    """Test CMS endpoints"""
    print("📝 Testing CMS endpoints...")
    try:
        # Test benefits
        response = requests.get(f"{BASE_URL}/api/v1/cms/benefits")
        if response.status_code == 200:
            benefits = response.json()
            print(f"✅ Found {len(benefits)} benefits")
        else:
            print(f"❌ Get benefits failed: {response.status_code}")
            return False
        
        # Test testimonials
        response = requests.get(f"{BASE_URL}/api/v1/cms/testimonials")
        if response.status_code == 200:
            testimonials = response.json()
            print(f"✅ Found {len(testimonials)} testimonials")
            return True
        else:
            print(f"❌ Get testimonials failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ CMS endpoints error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("🧪 PERIOD CARE BACKEND API TESTS")
    print("=" * 50)
    print()
    
    tests = [
        test_health_check,
        test_admin_login,
        test_user_login,
        test_get_kits,
        test_get_fruits,
        test_get_nutrients,
        test_create_order,
        test_admin_dashboard,
        test_benefits_and_testimonials
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The API is working correctly.")
    else:
        print(f"⚠️ {total - passed} tests failed. Please check the output above.")
    
    print("=" * 50)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
