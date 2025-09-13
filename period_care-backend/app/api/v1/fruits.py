from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.schemas.fruit import FruitResponse, FruitCreate, FruitUpdate, FruitList
from app.crud import fruit as fruit_crud
from app.api.v1.auth import get_current_admin_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[FruitList])
def get_all_fruits(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all available fruits"""
    fruits = fruit_crud.get_fruits(db, skip, limit, available_only=True)
    return fruits


@router.get("/{fruit_id}", response_model=FruitResponse)
def get_fruit_by_id(fruit_id: int, db: Session = Depends(get_db)):
    """Get specific fruit by ID"""
    fruit = fruit_crud.get_fruit_by_id(db, fruit_id)
    
    if not fruit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fruit not found"
        )
    
    return fruit


@router.post("/", response_model=FruitResponse)
def create_fruit(
    fruit_data: FruitCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Create new fruit (Admin only)"""
    fruit = fruit_crud.create_fruit(db, fruit_data)
    return fruit


@router.put("/{fruit_id}", response_model=FruitResponse)
def update_fruit(
    fruit_id: int,
    fruit_update: FruitUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Update fruit (Admin only)"""
    fruit = fruit_crud.update_fruit(db, fruit_id, fruit_update)
    
    if not fruit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fruit not found"
        )
    
    return fruit


@router.delete("/{fruit_id}")
def delete_fruit(
    fruit_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Delete fruit (Admin only)"""
    success = fruit_crud.delete_fruit(db, fruit_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fruit not found"
        )
    
    return {"message": "Fruit deleted successfully"}


@router.patch("/{fruit_id}/toggle-availability", response_model=FruitResponse)
def toggle_fruit_availability(
    fruit_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Toggle fruit availability (Admin only)"""
    fruit = fruit_crud.toggle_fruit_availability(db, fruit_id)
    
    if not fruit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fruit not found"
        )
    
    return fruit
