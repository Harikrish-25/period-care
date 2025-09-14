#!/usr/bin/env python3
"""
Test script to verify the order API endpoint works correctly
"""

import requests
import json

BASE_URL = "http://localhost:8001/api"

def test_order_creation():
    """Test the order creation endpoint"""
    
    # First, let's test with a sample order payload
    test_order = {
        "kit_id": "1",  # Assuming kit with ID 1 exists
        "selected_fruits": ["apple", "banana"],
        "selected_nutrients": ["vitamin_c", "iron"],
        "scheduled_date": "2025-09-20",
        "delivery_address": "123 Test Street, Test City"
    }
    
    # Test with a mock token
    headers = {
        "Authorization": "Bearer fake_token_user_1",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/orders", 
                               json=test_order, 
                               headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Order creation successful!")
            return True
        else:
            print("❌ Order creation failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_kits_endpoint():
    """Test the kits endpoint to see available kits"""
    try:
        response = requests.get(f"{BASE_URL}/kits")
        print(f"Available kits: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error getting kits: {e}")
        return False

if __name__ == "__main__":
    print("Testing Period Care API Endpoints...")
    print("=" * 50)
    
    print("\n1. Testing kits endpoint...")
    test_kits_endpoint()
    
    print("\n2. Testing order creation...")
    test_order_creation()