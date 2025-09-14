#!/usr/bin/env python3
"""
Direct test of WhatsApp functionality
"""

import os
import webbrowser
import urllib.parse

# Admin WhatsApp number
ADMIN_WHATSAPP = os.getenv('ADMIN_WHATSAPP', '917339625044')

def send_whatsapp_message(phone_number: str, message: str) -> bool:
    """Send WhatsApp message using system integration"""
    try:
        print(f"📱 SENDING REAL WhatsApp message to admin...")
        print(f"Phone: {phone_number}")
        print(f"Message: {message}")
        print("-" * 50)
        
        # Clean the phone number (remove any non-digits)
        clean_phone = ''.join(filter(str.isdigit, phone_number))
        
        # Ensure phone number starts with country code
        if not clean_phone.startswith('91'):
            clean_phone = '91' + clean_phone
        
        # URL encode the message
        encoded_message = urllib.parse.quote(message)
        
        # Create WhatsApp Web URL
        whatsapp_url = f"https://web.whatsapp.com/send?phone={clean_phone}&text={encoded_message}"
        
        print(f"Opening WhatsApp Web: {whatsapp_url}")
        
        # Open WhatsApp Web in default browser
        webbrowser.open(whatsapp_url)
        
        print(f"✅ WhatsApp Web opened successfully for {clean_phone}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending WhatsApp message: {str(e)}")
        return False

if __name__ == "__main__":
    # Test message
    message = """🔔 NEW ORDER RECEIVED (TEST)

Customer: Test Customer
Kit: Premium Care Kit
Quantity: 2
Total Amount: ₹1198

Please process this order promptly.
Period Care Admin"""
    
    print("Testing WhatsApp message sending...")
    result = send_whatsapp_message(ADMIN_WHATSAPP, message)
    print(f"Result: {result}")
    
    input("Press Enter to exit...")