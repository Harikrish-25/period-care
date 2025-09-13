from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, desc
from typing import Optional, List
from datetime import date, datetime
from app.models.reminder import Reminder
from app.schemas.reminder import ReminderCreate, ReminderUpdate


def get_reminder_by_id(db: Session, reminder_id: int) -> Optional[Reminder]:
    return db.query(Reminder).filter(Reminder.id == reminder_id).first()


def get_reminders(db: Session, skip: int = 0, limit: int = 100) -> List[Reminder]:
    return db.query(Reminder).options(
        joinedload(Reminder.user)
    ).order_by(desc(Reminder.created_at)).offset(skip).limit(limit).all()


def get_pending_reminders(db: Session) -> List[Reminder]:
    return db.query(Reminder).filter(
        Reminder.status == "pending"
    ).options(joinedload(Reminder.user)).all()


def get_reminders_by_status(db: Session, status: str) -> List[Reminder]:
    return db.query(Reminder).filter(
        Reminder.status == status
    ).options(joinedload(Reminder.user)).all()


def create_reminder(db: Session, reminder: ReminderCreate) -> Reminder:
    db_reminder = Reminder(**reminder.dict())
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder


def update_reminder(db: Session, reminder_id: int, reminder_update: ReminderUpdate) -> Optional[Reminder]:
    db_reminder = get_reminder_by_id(db, reminder_id)
    if not db_reminder:
        return None
    
    update_data = reminder_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_reminder, field, value)
    
    db.commit()
    db.refresh(db_reminder)
    return db_reminder


def mark_reminder_sent(db: Session, reminder_id: int) -> Optional[Reminder]:
    db_reminder = get_reminder_by_id(db, reminder_id)
    if not db_reminder:
        return None
    
    db_reminder.status = "sent"
    db_reminder.reminder_date = datetime.utcnow()
    db.commit()
    db.refresh(db_reminder)
    return db_reminder


def mark_reminder_completed(db: Session, reminder_id: int) -> Optional[Reminder]:
    db_reminder = get_reminder_by_id(db, reminder_id)
    if not db_reminder:
        return None
    
    db_reminder.status = "completed"
    db.commit()
    db.refresh(db_reminder)
    return db_reminder


def mark_admin_notified(db: Session, reminder_id: int) -> Optional[Reminder]:
    db_reminder = get_reminder_by_id(db, reminder_id)
    if not db_reminder:
        return None
    
    db_reminder.admin_notified = True
    db.commit()
    db.refresh(db_reminder)
    return db_reminder


def get_user_reminders(db: Session, user_id: int) -> List[Reminder]:
    return db.query(Reminder).filter(
        Reminder.user_id == user_id
    ).order_by(desc(Reminder.created_at)).all()


def get_reminders_for_date(db: Session, target_date: date) -> List[Reminder]:
    return db.query(Reminder).filter(
        Reminder.last_order_date == target_date
    ).options(joinedload(Reminder.user)).all()


def delete_old_reminders(db: Session, before_date: datetime) -> int:
    """Delete completed reminders older than specified date"""
    count = db.query(Reminder).filter(
        and_(
            Reminder.status == "completed",
            Reminder.created_at < before_date
        )
    ).count()
    
    db.query(Reminder).filter(
        and_(
            Reminder.status == "completed",
            Reminder.created_at < before_date
        )
    ).delete()
    
    db.commit()
    return count
