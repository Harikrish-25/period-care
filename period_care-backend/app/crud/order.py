from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, desc
from typing import Optional, List
from datetime import date
from app.models.order import Order
from app.models.user import User
from app.models.kit import Kit
from app.schemas.order import OrderCreate, OrderUpdate


def get_order_by_id(db: Session, order_id: int) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[Order]:
    return db.query(Order).options(
        joinedload(Order.user),
        joinedload(Order.kit)
    ).order_by(desc(Order.created_at)).offset(skip).limit(limit).all()


def get_user_orders(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Order]:
    return db.query(Order).filter(Order.user_id == user_id).options(
        joinedload(Order.kit)
    ).order_by(desc(Order.created_at)).offset(skip).limit(limit).all()


def create_order(db: Session, order: OrderCreate, user_id: int, total_amount: float) -> Order:
    db_order = Order(
        user_id=user_id,
        kit_id=order.kit_id,
        selected_fruits=order.selected_fruits,
        selected_nutrients=order.selected_nutrients,
        scheduled_date=order.scheduled_date,
        delivery_address=order.delivery_address,
        total_amount=total_amount
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order(db: Session, order_id: int, order_update: OrderUpdate) -> Optional[Order]:
    db_order = get_order_by_id(db, order_id)
    if not db_order:
        return None
    
    update_data = order_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_order, field, value)
    
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order_status(db: Session, order_id: int, status: str) -> Optional[Order]:
    db_order = get_order_by_id(db, order_id)
    if not db_order:
        return None
    
    db_order.status = status
    db.commit()
    db.refresh(db_order)
    return db_order


def mark_whatsapp_sent(db: Session, order_id: int) -> Optional[Order]:
    db_order = get_order_by_id(db, order_id)
    if not db_order:
        return None
    
    db_order.whatsapp_sent = True
    db.commit()
    db.refresh(db_order)
    return db_order


def get_orders_by_status(db: Session, status: str, skip: int = 0, limit: int = 100) -> List[Order]:
    return db.query(Order).filter(Order.status == status).options(
        joinedload(Order.user),
        joinedload(Order.kit)
    ).order_by(desc(Order.created_at)).offset(skip).limit(limit).all()


def get_orders_by_date_range(db: Session, start_date: date, end_date: date) -> List[Order]:
    return db.query(Order).filter(
        and_(
            Order.created_at >= start_date,
            Order.created_at <= end_date
        )
    ).options(
        joinedload(Order.user),
        joinedload(Order.kit)
    ).all()


def get_order_with_details(db: Session, order_id: int):
    """Get order with user and kit details"""
    return db.query(Order).filter(Order.id == order_id).options(
        joinedload(Order.user),
        joinedload(Order.kit)
    ).first()
