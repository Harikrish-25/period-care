from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.schemas.reminder import ReminderResponse, ReminderWithUser, ReminderUpdate
from app.services.reminder_service import ReminderService
from app.crud import reminder as reminder_crud, user as user_crud
from app.api.v1.auth import get_current_admin_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[ReminderWithUser])
def get_pending_reminders(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Get all pending reminders (Admin only)"""
    reminder_service = ReminderService(db)
    reminders = reminder_service.get_pending_reminders()
    
    # Transform to include user details
    reminder_details = []
    for reminder in reminders:
        reminder_details.append({
            "id": reminder.id,
            "user_id": reminder.user_id,
            "user_name": reminder.user.name,
            "user_email": reminder.user.email,
            "user_mobile": reminder.user.mobile,
            "reminder_type": reminder.reminder_type,
            "last_order_date": reminder.last_order_date,
            "reminder_date": reminder.reminder_date,
            "status": reminder.status,
            "admin_notified": reminder.admin_notified
        })
    
    return reminder_details


@router.post("/send")
def send_reminders_manually(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Manually trigger reminder sending (Admin only)"""
    reminder_service = ReminderService(db)
    results = reminder_service.check_and_send_reminders()
    
    return {
        "message": "Reminders processed successfully",
        "results": results
    }


@router.get("/users-due", response_model=List[dict])
def get_users_due_for_reminder(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Get users due for reminders (Admin only)"""
    reminder_service = ReminderService(db)
    users = reminder_service.get_users_due_for_reminder()
    
    # Transform to include relevant details
    user_details = []
    for user in users:
        user_details.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "mobile": user.mobile,
            "last_order_date": user.last_order_date,
            "reminder_sent": user.reminder_sent
        })
    
    return user_details


@router.put("/{reminder_id}/complete", response_model=ReminderResponse)
def mark_reminder_completed(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Mark reminder as completed (Admin only)"""
    reminder_service = ReminderService(db)
    success = reminder_service.mark_reminder_completed(reminder_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )
    
    reminder = reminder_crud.get_reminder_by_id(db, reminder_id)
    return reminder


@router.post("/send-manual/{user_id}")
def send_manual_reminder(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Send manual reminder to specific user (Admin only)"""
    reminder_service = ReminderService(db)
    success = reminder_service.send_manual_reminder(user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or reminder failed to send"
        )
    
    return {"message": f"Manual reminder sent to user {user_id}"}


@router.post("/cleanup")
def cleanup_old_reminders(
    days_old: int = 90,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Clean up old completed reminders (Admin only)"""
    reminder_service = ReminderService(db)
    cleaned_count = reminder_service.cleanup_old_reminders(days_old)
    
    return {
        "message": f"Cleaned up {cleaned_count} old reminder records",
        "cleaned_count": cleaned_count
    }


@router.get("/stats")
def get_reminder_statistics(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Get reminder statistics (Admin only)"""
    pending_reminders = reminder_crud.get_reminders_by_status(db, "pending")
    sent_reminders = reminder_crud.get_reminders_by_status(db, "sent")
    completed_reminders = reminder_crud.get_reminders_by_status(db, "completed")
    
    reminder_service = ReminderService(db)
    users_due = reminder_service.get_users_due_for_reminder()
    
    return {
        "pending_reminders": len(pending_reminders),
        "sent_reminders": len(sent_reminders),
        "completed_reminders": len(completed_reminders),
        "users_due_for_reminder": len(users_due),
        "total_reminders": len(pending_reminders) + len(sent_reminders) + len(completed_reminders)
    }
