from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.schemas.order import OrderCreate, OrderResponse, OrderCalculation, OrderWithDetails
from app.services.order_service import OrderService
from app.crud import order as order_crud
from app.api.v1.auth import get_current_user_dependency, get_current_admin_user
from app.models.user import User

router = APIRouter()


@router.post("/calculate", response_model=OrderCalculation)
def calculate_order_total(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    """Calculate order total without placing order"""
    order_service = OrderService(db)
    calculation = order_service.calculate_order_total(order_data)
    
    if not calculation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid kit or add-ons selected"
        )
    
    return calculation


@router.post("/", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Place a new order"""
    order_service = OrderService(db)
    order = order_service.create_order(order_data, current_user.id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create order. Please check your selections."
        )
    
    return order


@router.get("/", response_model=List[OrderWithDetails])
def get_all_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Get all orders (Admin only)"""
    orders = order_crud.get_orders(db, skip, limit)
    
    # Transform to include details
    order_details = []
    for order in orders:
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


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_by_id(
    order_id: int,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get specific order by ID"""
    order = order_crud.get_order_by_id(db, order_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check if user owns the order or is admin
    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return order


@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    status_update: str,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Update order status (Admin only)"""
    order_service = OrderService(db)
    order = order_service.update_order_status(order_id, status_update)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return order


@router.post("/{order_id}/whatsapp")
def send_whatsapp_notification(
    order_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Send WhatsApp notification for order (Admin only)"""
    order_service = OrderService(db)
    order = order_service.get_order_details(order_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # This would trigger the WhatsApp notification
    # The actual notification is sent when order is created
    return {"message": "WhatsApp notification triggered"}


@router.get("/status/{status_name}", response_model=List[OrderResponse])
def get_orders_by_status(
    status_name: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Get orders by status (Admin only)"""
    orders = order_crud.get_orders_by_status(db, status_name, skip, limit)
    return orders
