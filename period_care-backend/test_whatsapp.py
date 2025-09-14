#!/usr/bin/env python3
"""
Test script for WhatsApp integration
"""

import requests
import json

# Test server connection
def test_server():
    try:
        response = requests.get("http://localhost:8000/")
        print("✅ Server is running:", response.json())
        return True
    except Exception as e:
        print("❌ Server connection failed:", e)
        return False

# Test login
def test_login():
    try:
        data = {
            "username": "admin@periodcare.com",
            "password": "admin123"
        }
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            headers={"Content-Type": "application/json"},
            json=data
        )
        if response.status_code == 200:
            result = response.json()
            print("✅ Login successful!")
            print(f"Token: {result.get('access_token', 'No token')}")
            return result.get('access_token')
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print("❌ Login error:", e)
        return None

# Test order creation with WhatsApp
def test_order_creation(token):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        data = {
            "kit_id": "1",
            "selected_fruits": ["apple", "banana"],
            "selected_nutrients": ["vitamin-c", "iron"],
            "scheduled_date": "2024-01-15",
            "delivery_address": "123 Test Street, Test City, 12345"
        }
        
        response = requests.post(
            "http://localhost:8000/api/v1/orders/",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            print("✅ Order created successfully!")
            print(f"Order ID: {result.get('id')}")
            print(f"WhatsApp Web URL: {result.get('whatsapp_web_url', 'Not available')}")
            print(f"WhatsApp Mobile URL: {result.get('whatsapp_mobile_url', 'Not available')}")
            print(f"Admin Contact: {result.get('admin_contact', 'Not available')}")
            return result
        else:
            print(f"❌ Order creation failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print("❌ Order creation error:", e)
        return None

if __name__ == "__main__":
    print("🚀 Testing WhatsApp Integration...")
    print("-" * 50)
    
    # Test server
    if not test_server():
        print("Please start the server first: python simple_server.py")
        exit(1)
    
    print("-" * 50)
    
    # Test login
    token = test_login()
    if not token:
        print("Login failed. Please check credentials.")
        exit(1)
    
    print("-" * 50)
    
    # Test order creation
    order = test_order_creation(token)
    if order:
        print("\n🎉 WhatsApp Integration Test Complete!")
        print("✅ All tests passed!")
        
        # Print WhatsApp links for manual testing
        if order.get('whatsapp_web_url'):
            print(f"\n📱 Test WhatsApp Web: {order['whatsapp_web_url']}")
        if order.get('whatsapp_mobile_url'):
            print(f"📱 Test WhatsApp Mobile: {order['whatsapp_mobile_url']}")
    else:
        print("❌ Order creation failed.")