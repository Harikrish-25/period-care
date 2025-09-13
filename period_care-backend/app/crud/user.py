from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from datetime import datetime, date
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.config.security import get_password_hash, verify_password


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        mobile=user.mobile,
        address=user.address,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return None
    return user


def update_user_last_order_date(db: Session, user_id: int, order_date: date) -> Optional[User]:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    db_user.last_order_date = order_date
    db_user.reminder_sent = False  # Reset reminder flag when new order is placed
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users_due_for_reminder(db: Session, target_date: date) -> List[User]:
    """Get users who last ordered on the target date (30 days ago)"""
    return db.query(User).filter(
        and_(
            User.last_order_date == target_date,
            User.reminder_sent == False,
            User.is_active == True
        )
    ).all()


def mark_user_reminder_sent(db: Session, user_id: int) -> Optional[User]:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    db_user.reminder_sent = True
    db.commit()
    db.refresh(db_user)
    return db_user


def toggle_user_status(db: Session, user_id: int) -> Optional[User]:
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    db_user.is_active = not db_user.is_active
    db.commit()
    db.refresh(db_user)
    return db_user
