#!/usr/bin/env python3
"""
Test script to verify the direct WhatsApp messaging works
"""

import requests
import json

BASE_URL = "http://localhost:8001/api"

def test_direct_whatsapp():
    """Test the direct WhatsApp messaging by placing an order"""
    
    # Test order payload
    test_order = {
        "kit_id": "1",
        "selected_fruits": ["apple"],
        "selected_nutrients": ["vitamin_c"],
        "scheduled_date": "2025-09-20",
        "delivery_address": "Test Address for Direct WhatsApp"
    }
    
    # Test with a mock token
    headers = {
        "Authorization": "Bearer fake_token_user_1",
        "Content-Type": "application/json"
    }
    
    try:
        print("Testing direct WhatsApp messaging...")
        print("When you run this test, WhatsApp Web should open automatically!")
        print("-" * 60)
        
        response = requests.post(f"{BASE_URL}/orders", 
                               json=test_order, 
                               headers=headers)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Order created successfully!")
            print(f"Order ID: {result.get('id')}")
            print(f"Total Amount: ₹{result.get('totalAmount')}")
            print(f"WhatsApp Status: {'✅ Sent' if result.get('whatsapp_sent') else '❌ Failed'}")
            print("\n🎉 WhatsApp Web should have opened automatically with the order message!")
            return True
        else:
            print(f"❌ Order creation failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_direct_whatsapp()