from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.schemas.user import UserProfile, UserUpdate
from app.schemas.order import OrderResponse
from app.crud import user as user_crud, order as order_crud
from app.api.v1.auth import get_current_user_dependency
from app.models.user import User

router = APIRouter()


@router.get("/profile", response_model=UserProfile)
def get_user_profile(current_user: User = Depends(get_current_user_dependency)):
    """Get current user profile"""
    return current_user


@router.put("/profile", response_model=UserProfile)
def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    updated_user = user_crud.update_user(db, current_user.id, user_update)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user


@router.get("/orders", response_model=List[OrderResponse])
def get_user_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get current user's orders"""
    orders = order_crud.get_user_orders(db, current_user.id, skip, limit)
    return orders


@router.get("/order-history", response_model=List[OrderResponse])
def get_user_order_history(
    current_user: User = Depends(get_current_user_dependency),
    db: Session = Depends(get_db)
):
    """Get current user's order history"""
    orders = order_crud.get_user_orders(db, current_user.id, 0, 1000)
    return orders
