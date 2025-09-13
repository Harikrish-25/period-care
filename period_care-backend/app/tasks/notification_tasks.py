from datetime import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.services.notification_service import NotificationService
from app.services.whatsapp_service import WhatsAppService


def get_db_session():
    """Get database session"""
    return SessionLocal()


def send_order_notification(order_data: Dict[str, Any]) -> bool:
    """Background task to send order notification"""
    try:
        whatsapp_service = WhatsAppService()
        notification_service = NotificationService()
        
        # Send WhatsApp to admin
        whatsapp_sent = whatsapp_service.send_order_notification(order_data)
        
        # Send email confirmation to customer
        email_sent = notification_service.send_order_confirmation(
            order_data.get('customer_email'),
            order_data.get('customer_name'),
            order_data
        )
        
        print(f"📲 Order notification sent - WhatsApp: {whatsapp_sent}, Email: {email_sent}")
        return whatsapp_sent or email_sent
        
    except Exception as e:
        print(f"❌ Failed to send order notification: {e}")
        return False


def send_welcome_notification(user_data: Dict[str, Any]) -> bool:
    """Background task to send welcome notification"""
    try:
        notification_service = NotificationService()
        
        email_sent = notification_service.send_welcome_email(
            user_data.get('email'),
            user_data.get('name')
        )
        
        print(f"📧 Welcome email sent: {email_sent}")
        return email_sent
        
    except Exception as e:
        print(f"❌ Failed to send welcome notification: {e}")
        return False


def send_bulk_reminder_notifications(users_data: list) -> Dict[str, int]:
    """Background task to send bulk reminder notifications"""
    try:
        notification_service = NotificationService()
        whatsapp_service = WhatsAppService()
        
        # Send email reminders
        email_results = notification_service.send_bulk_reminders(users_data)
        
        # Send WhatsApp reminders
        whatsapp_sent = 0
        for user in users_data:
            success = whatsapp_service.send_reminder_notification(user)
            if success:
                whatsapp_sent += 1
        
        results = {
            "total_users": len(users_data),
            "emails_sent": email_results.get("sent", 0),
            "emails_failed": email_results.get("failed", 0),
            "whatsapp_sent": whatsapp_sent,
            "whatsapp_failed": len(users_data) - whatsapp_sent
        }
        
        print(f"📱 Bulk reminders sent: {results}")
        return results
        
    except Exception as e:
        print(f"❌ Failed to send bulk reminders: {e}")
        return {"error": str(e)}


def log_system_event(event_type: str, message: str, data: Dict[str, Any] = None):
    """Log system events for monitoring"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {event_type}: {message}"
    
    if data:
        log_entry += f" | Data: {data}"
    
    print(log_entry)
    
    # In production, you might want to write to a log file or send to a logging service
