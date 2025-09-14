#!/usr/bin/env python3
"""
Minimal test server to debug WhatsApp integration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import webbrowser
import urllib.parse

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Admin WhatsApp number
ADMIN_WHATSAPP = os.getenv('ADMIN_WHATSAPP', '917339625044')

class OrderRequest(BaseModel):
    user_name: str
    kit_name: str
    quantity: int = 1
    price: float

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

@app.get("/")
def read_root():
    return {"message": "Period Care Test API Server is running!", "admin_whatsapp": ADMIN_WHATSAPP}

@app.post("/api/test-order")
def create_test_order(order: OrderRequest):
    """Create a test order and send WhatsApp notification to admin"""
    
    # Calculate total amount
    total_amount = order.price * order.quantity
    
    # Create order message
    message = f"""🔔 NEW ORDER RECEIVED (TEST)

Customer: {order.user_name}
Kit: {order.kit_name}
Quantity: {order.quantity}
Total Amount: ₹{total_amount}

Please process this order promptly.
Period Care Admin"""
    
    # Send WhatsApp message to admin
    whatsapp_sent = send_whatsapp_message(ADMIN_WHATSAPP, message)
    
    return {
        "message": "Order placed successfully!",
        "total_amount": total_amount,
        "whatsapp_sent": whatsapp_sent,
        "admin_phone": ADMIN_WHATSAPP
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting Period Care Test API Server...")
    print(f"Admin WhatsApp: {ADMIN_WHATSAPP}")
    uvicorn.run(app, host="127.0.0.1", port=8002)