import schedule
import time
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.services.reminder_service import ReminderService
from app.config.settings import settings


def get_db_session():
    """Get database session"""
    return SessionLocal()


def daily_reminder_check():
    """Daily task to check and send reminders"""
    print(f"🕐 Running daily reminder check at {datetime.now()}")
    
    db = get_db_session()
    try:
        reminder_service = ReminderService(db)
        results = reminder_service.check_and_send_reminders()
        
        print(f"📊 Reminder Check Results:")
        print(f"   • Users found: {results['users_found']}")
        print(f"   • Reminders sent: {results['reminders_sent']}")
        print(f"   • Emails sent: {results['emails_sent']}")
        print(f"   • WhatsApp sent: {results['whatsapp_sent']}")
        print(f"   • Admin notified: {results['admin_notified']}")
        
    except Exception as e:
        print(f"❌ Error in daily reminder check: {e}")
    finally:
        db.close()


def weekly_cleanup():
    """Weekly task to clean up old reminders"""
    print(f"🧹 Running weekly cleanup at {datetime.now()}")
    
    db = get_db_session()
    try:
        reminder_service = ReminderService(db)
        cleaned_count = reminder_service.cleanup_old_reminders(days_old=90)
        print(f"🗑️ Cleaned up {cleaned_count} old reminder records")
        
    except Exception as e:
        print(f"❌ Error in weekly cleanup: {e}")
    finally:
        db.close()


def schedule_tasks():
    """Schedule all background tasks"""
    # Parse reminder check time from settings
    reminder_time = settings.reminder_check_time  # Format: "09:00"
    
    # Schedule daily reminder check
    schedule.every().day.at(reminder_time).do(daily_reminder_check)
    
    # Schedule weekly cleanup (every Sunday at 2 AM)
    schedule.every().sunday.at("02:00").do(weekly_cleanup)
    
    print(f"📅 Scheduled tasks:")
    print(f"   • Daily reminder check: {reminder_time}")
    print(f"   • Weekly cleanup: Sunday 02:00")


def run_scheduler():
    """Run the task scheduler"""
    schedule_tasks()
    
    print("🚀 Background task scheduler started")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n🛑 Background task scheduler stopped")


if __name__ == "__main__":
    run_scheduler()
