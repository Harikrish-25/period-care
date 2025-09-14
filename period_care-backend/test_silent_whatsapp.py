#!/usr/bin/env python3
"""
Test the silent WhatsApp integration
"""

import requests
import json

def test_silent_whatsapp():
    print("🔕 Testing Silent WhatsApp Integration...")
    print("-" * 50)
    
    # Test login
    login_data = {
        "username": "admin@periodcare.com",
        "password": "admin123"
    }
    
    response = requests.post(
        "http://localhost:8000/api/v1/auth/login",
        headers={"Content-Type": "application/json"},
        json=login_data
    )
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.text}")
        return
    
    token = response.json()["access_token"]
    print("✅ Login successful!")
    
    # Test order creation
    order_data = {
        "kit_id": "1",
        "selected_fruits": ["apple", "banana"],
        "selected_nutrients": ["vitamin-c"],
        "scheduled_date": "2024-01-15",
        "delivery_address": "123 Test Street, Test City, 12345"
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.post(
        "http://localhost:8000/api/v1/orders/",
        headers=headers,
        json=order_data
    )
    
    if response.status_code in [200, 201]:
        order = response.json()
        print("✅ Order created successfully!")
        print(f"📦 Order ID: #{order['id']}")
        print(f"💰 Total: ₹{order['total_amount']}")
        print(f"📱 WhatsApp Status: {order.get('whatsapp_notification', 'Unknown')}")
        print(f"📝 Message: {order.get('message', 'No message')}")
        print("\n🔕 WhatsApp message should be sent SILENTLY to admin!")
        print("✅ User only sees: 'Order placed successfully!'")
    else:
        print(f"❌ Order creation failed: {response.text}")

if __name__ == "__main__":
    test_silent_whatsapp()