from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta
from app.config.database import get_db
from app.schemas.user import UserResponse
from app.schemas.order import OrderWithDetails
from app.crud import user as user_crud, order as order_crud, kit as kit_crud, fruit as fruit_crud, nutrient as nutrient_crud
from app.api.v1.auth import get_current_admin_user
from app.models.user import User

router = APIRouter()


@router.get("/dashboard/stats")
def get_dashboard_statistics(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Get dashboard statistics (Admin only)"""
    
    # Get current date ranges
    today = date.today()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Total users
    total_users = len(user_crud.get_users(db, 0, 10000))
    active_users = len([u for u in user_crud.get_users(db, 0, 10000) if u.is_active])
    
    # Orders statistics
    all_orders = order_crud.get_orders(db, 0, 10000)
    total_orders = len(all_orders)
    
    pending_orders = len(order_crud.get_orders_by_status(db, "pending", 0, 1000))
    completed_orders = len(order_crud.get_orders_by_status(db, "completed", 0, 1000))
    cancelled_orders = len(order_crud.get_orders_by_status(db, "cancelled", 0, 1000))
    
    # Revenue calculation
    total_revenue = sum(order.total_amount for order in all_orders if order.status == "completed")
    
    # Recent orders (last 7 days)
    recent_orders = [o for o in all_orders if o.created_at.date() >= week_ago]
    weekly_revenue = sum(order.total_amount for order in recent_orders if order.status == "completed")
    
    # Monthly stats
    monthly_orders = [o for o in all_orders if o.created_at.date() >= month_ago]
    monthly_revenue = sum(order.total_amount for order in monthly_orders if order.status == "completed")
    
    # Product statistics
    total_kits = len(kit_crud.get_kits(db, 0, 1000, available_only=False))
    available_kits = len(kit_crud.get_kits(db, 0, 1000, available_only=True))
    
    total_fruits = len(fruit_crud.get_fruits(db, 0, 1000, available_only=False))
    available_fruits = len(fruit_crud.get_fruits(db, 0, 1000, available_only=True))
    
    total_nutrients = len(nutrient_crud.get_nutrients(db, 0, 1000, available_only=False))
    available_nutrients = len(nutrient_crud.get_nutrients(db, 0, 1000, available_only=True))
    
    # Users due for reminder
    reminder_due_date = today - timedelta(days=30)
    users_due_reminder = len(user_crud.get_users_due_for_reminder(db, reminder_due_date))
    
    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "inactive": total_users - active_users,
            "due_for_reminder": users_due_reminder
        },
        "orders": {
            "total": total_orders,
            "pending": pending_orders,
            "completed": completed_orders,
            "cancelled": cancelled_orders,
            "this_week": len(recent_orders),
            "this_month": len(monthly_orders)
        },
        "revenue": {
            "total": total_revenue,
            "this_week": weekly_revenue,
            "this_month": monthly_revenue,
            "average_order_value": total_revenue / total_orders if total_orders > 0 else 0
        },
        "products": {
            "kits": {"total": total_kits, "available": available_kits},
            "fruits": {"total": total_fruits, "available": available_fruits},
            "nutrients": {"total": total_nutrients, "available": available_nutrients}
        }
    }


@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Get all users (Admin only)"""
    users = user_crud.get_users(db, skip, limit)
    return users


@router.get("/users-due-reminder")
def get_users_due_reminder(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Get users who need reminders (Admin only)"""
    reminder_due_date = date.today() - timedelta(days=30)
    users = user_crud.get_users_due_for_reminder(db, reminder_due_date)
    
    user_details = []
    for user in users:
        user_details.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "mobile": user.mobile,
            "last_order_date": user.last_order_date,
            "reminder_sent": user.reminder_sent,
            "days_since_order": (date.today() - user.last_order_date).days if user.last_order_date else None
        })
    
    return {
        "users_count": len(user_details),
        "users": user_details
    }


@router.put("/users/{user_id}/status", response_model=UserResponse)
def toggle_user_status(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Activate/deactivate user (Admin only)"""
    user = user_crud.toggle_user_status(db, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.get("/orders/recent", response_model=List[OrderWithDetails])
def get_recent_orders(
    days: int = 7,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Get recent orders (Admin only)"""
    start_date = date.today() - timedelta(days=days)
    orders = order_crud.get_orders_by_date_range(db, start_date, date.today())
    
    # Limit and transform results
    limited_orders = orders[:limit]
    order_details = []
    
    for order in limited_orders:
        order_details.append({
            "id": order.id,
            "user_id": order.user_id,
            "kit_id": order.kit_id,
            "kit_name": order.kit.name,
            "kit_type": order.kit.type,
            "kit_base_price": order.kit.base_price,
            "user_name": order.user.name,
            "user_email": order.user.email,
            "user_mobile": order.user.mobile,
            "selected_fruits": order.selected_fruits,
            "selected_nutrients": order.selected_nutrients,
            "scheduled_date": order.scheduled_date,
            "delivery_address": order.delivery_address,
            "total_amount": order.total_amount,
            "status": order.status,
            "whatsapp_sent": order.whatsapp_sent,
            "created_at": order.created_at
        })
    
    return order_details


@router.get("/analytics/top-products")
def get_top_products(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Get top selling products analytics (Admin only)"""
    # This is a simplified version - you might want to implement more sophisticated analytics
    orders = order_crud.get_orders(db, 0, 10000)
    
    kit_sales = {}
    for order in orders:
        if order.status == "completed":
            kit_name = order.kit.name
            kit_sales[kit_name] = kit_sales.get(kit_name, 0) + 1
    
    # Sort by sales count
    top_kits = sorted(kit_sales.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        "top_kits": [{"name": name, "sales": count} for name, count in top_kits],
        "total_completed_orders": len([o for o in orders if o.status == "completed"])
    }
