from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import date, datetime, timedelta
from app.crud import user as user_crud, reminder as reminder_crud, order as order_crud
from app.schemas.reminder import ReminderCreate
from app.services.whatsapp_service import WhatsAppService
from app.services.notification_service import NotificationService


class ReminderService:
    def __init__(self, db: Session):
        self.db = db
        self.whatsapp_service = WhatsAppService()
        self.notification_service = NotificationService()
    
    def check_and_send_reminders(self) -> Dict[str, int]:
        """Check for users due for reminders and send them"""
        # Calculate date 30 days ago
        target_date = date.today() - timedelta(days=30)
        
        # Get users who ordered exactly 30 days ago and haven't been reminded
        users_due = user_crud.get_users_due_for_reminder(self.db, target_date)
        
        results = {
            "users_found": len(users_due),
            "reminders_sent": 0,
            "emails_sent": 0,
            "whatsapp_sent": 0,
            "admin_notified": 0
        }
        
        reminder_list = []
        
        for user in users_due:
            try:
                # Create reminder record
                reminder_data = ReminderCreate(
                    user_id=user.id,
                    reminder_type="monthly_reorder",
                    last_order_date=user.last_order_date
                )
                reminder = reminder_crud.create_reminder(self.db, reminder_data)
                
                # Send email reminder
                email_sent = self.notification_service.send_reminder_email(
                    user.email,
                    user.name,
                    user.last_order_date.strftime("%Y-%m-%d")
                )
                
                # Send WhatsApp reminder
                user_data = {
                    "name": user.name,
                    "mobile": user.mobile,
                    "last_kit_name": "Period Care Kit",  # You might want to get actual kit name
                    "last_order_date": user.last_order_date.strftime("%Y-%m-%d")
                }
                whatsapp_sent = self.whatsapp_service.send_reminder_notification(user_data)
                
                # Mark reminder as sent
                if email_sent or whatsapp_sent:
                    reminder_crud.mark_reminder_sent(self.db, reminder.id)
                    user_crud.mark_user_reminder_sent(self.db, user.id)
                    results["reminders_sent"] += 1
                
                if email_sent:
                    results["emails_sent"] += 1
                if whatsapp_sent:
                    results["whatsapp_sent"] += 1
                
                # Add to admin notification list
                reminder_list.append({
                    "name": user.name,
                    "email": user.email,
                    "mobile": user.mobile,
                    "last_order_date": user.last_order_date.strftime("%Y-%m-%d"),
                    "last_kit_name": "Period Care Kit"
                })
                
            except Exception as e:
                print(f"Failed to send reminder to user {user.id}: {e}")
        
        # Send admin notification if there are reminders
        if reminder_list:
            admin_notified = self.whatsapp_service.send_admin_reminder_alert(reminder_list)
            if admin_notified:
                results["admin_notified"] = 1
        
        return results
    
    def get_pending_reminders(self) -> List:
        """Get all pending reminders"""
        return reminder_crud.get_pending_reminders(self.db)
    
    def get_users_due_for_reminder(self) -> List:
        """Get users who are due for reminders"""
        target_date = date.today() - timedelta(days=30)
        return user_crud.get_users_due_for_reminder(self.db, target_date)
    
    def mark_reminder_completed(self, reminder_id: int) -> bool:
        """Mark a reminder as completed"""
        reminder = reminder_crud.mark_reminder_completed(self.db, reminder_id)
        return reminder is not None
    
    def cleanup_old_reminders(self, days_old: int = 90) -> int:
        """Clean up old completed reminders"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        return reminder_crud.delete_old_reminders(self.db, cutoff_date)
    
    def send_manual_reminder(self, user_id: int) -> bool:
        """Manually send reminder to a specific user"""
        user = user_crud.get_user_by_id(self.db, user_id)
        if not user:
            return False
        
        try:
            # Send email reminder
            email_sent = self.notification_service.send_reminder_email(
                user.email,
                user.name,
                user.last_order_date.strftime("%Y-%m-%d") if user.last_order_date else "N/A"
            )
            
            # Send WhatsApp reminder
            user_data = {
                "name": user.name,
                "mobile": user.mobile,
                "last_kit_name": "Period Care Kit",
                "last_order_date": user.last_order_date.strftime("%Y-%m-%d") if user.last_order_date else "N/A"
            }
            whatsapp_sent = self.whatsapp_service.send_reminder_notification(user_data)
            
            # Create reminder record
            if email_sent or whatsapp_sent:
                reminder_data = ReminderCreate(
                    user_id=user.id,
                    reminder_type="manual_reminder",
                    last_order_date=user.last_order_date or date.today()
                )
                reminder = reminder_crud.create_reminder(self.db, reminder_data)
                reminder_crud.mark_reminder_sent(self.db, reminder.id)
                user_crud.mark_user_reminder_sent(self.db, user.id)
                return True
            
            return False
            
        except Exception as e:
            print(f"Failed to send manual reminder to user {user_id}: {e}")
            return False
