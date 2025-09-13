from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.services.whatsapp_service import WhatsAppService
from app.api.v1.auth import get_current_admin_user
from app.models.user import User

router = APIRouter()


@router.post("/send-message")
def send_whatsapp_message(
    phone_number: str,
    message: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Send WhatsApp message (Admin only)"""
    whatsapp_service = WhatsAppService()
    success = whatsapp_service.send_message(message, phone_number)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send WhatsApp message"
        )
    
    return {"message": "WhatsApp message sent successfully"}


@router.post("/test-admin-notification")
def test_admin_notification(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Test admin WhatsApp notification (Admin only)"""
    whatsapp_service = WhatsAppService()
    
    # Sample order data for testing
    test_order = {
        "id": "TEST123",
        "customer_name": "Test Customer",
        "customer_mobile": "+919876543210",
        "customer_email": "test@example.com",
        "kit_name": "Premium Wellness Kit",
        "kit_price": 799,
        "fruits": "🍎 Apple Slices, 🍌 Banana Chips",
        "nutrients": "Iron Supplement, Magnesium Complex",
        "order_date": "2025-09-11 14:30",
        "delivery_date": "2025-09-15",
        "delivery_address": "123 Test Street, Mumbai",
        "total_amount": 1089
    }
    
    success = whatsapp_service.send_order_notification(test_order)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send test notification"
        )
    
    return {"message": "Test WhatsApp notification sent successfully"}


@router.post("/test-reminder-notification")
def test_reminder_notification(
    phone_number: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Test reminder WhatsApp notification (Admin only)"""
    whatsapp_service = WhatsAppService()
    
    # Sample user data for testing
    test_user = {
        "name": "Test User",
        "mobile": phone_number,
        "last_kit_name": "Comfort Care Kit",
        "last_order_date": "2025-08-11"
    }
    
    success = whatsapp_service.send_reminder_notification(test_user)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send test reminder"
        )
    
    return {"message": "Test reminder notification sent successfully"}


@router.get("/integration-guide")
def get_whatsapp_integration_guide():
    """Get WhatsApp integration guide"""
    return {
        "title": "WhatsApp Integration Guide",
        "description": "How to integrate WhatsApp Business API",
        "steps": [
            {
                "step": 1,
                "title": "Get WhatsApp Business API Access",
                "description": "Apply for WhatsApp Business API through Meta or a BSP (Business Solution Provider)"
            },
            {
                "step": 2,
                "title": "Choose Integration Method",
                "options": [
                    {
                        "name": "Twilio",
                        "description": "Use Twilio's WhatsApp Business API",
                        "endpoint": "https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json"
                    },
                    {
                        "name": "Meta Cloud API",
                        "description": "Direct integration with Meta's Cloud API",
                        "endpoint": "https://graph.facebook.com/v17.0/{phone_number_id}/messages"
                    },
                    {
                        "name": "360Dialog",
                        "description": "European WhatsApp Business API provider",
                        "endpoint": "https://waba.360dialog.io/v1/messages"
                    }
                ]
            },
            {
                "step": 3,
                "title": "Update WhatsApp Service",
                "description": "Replace the placeholder implementation in app/services/whatsapp_service.py with actual API calls"
            },
            {
                "step": 4,
                "title": "Add Environment Variables",
                "variables": [
                    "WHATSAPP_API_URL",
                    "WHATSAPP_ACCESS_TOKEN",
                    "WHATSAPP_PHONE_NUMBER_ID",
                    "WHATSAPP_VERIFY_TOKEN"
                ]
            }
        ],
        "current_status": "Placeholder implementation - prints messages to console",
        "production_requirements": [
            "Valid WhatsApp Business Account",
            "Verified business profile",
            "Approved message templates",
            "API credentials and tokens"
        ]
    }
