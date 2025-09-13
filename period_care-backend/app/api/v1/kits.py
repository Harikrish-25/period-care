from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.schemas.kit import KitResponse, KitCreate, KitUpdate, KitList
from app.crud import kit as kit_crud
from app.api.v1.auth import get_current_admin_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[KitList])
def get_all_kits(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all available kits"""
    kits = kit_crud.get_kits(db, skip, limit, available_only=True)
    return kits


@router.get("/{kit_id}", response_model=KitResponse)
def get_kit_by_id(kit_id: int, db: Session = Depends(get_db)):
    """Get specific kit by ID"""
    kit = kit_crud.get_kit_by_id(db, kit_id)
    
    if not kit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kit not found"
        )
    
    return kit


@router.post("/", response_model=KitResponse)
def create_kit(
    kit_data: KitCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Create new kit (Admin only)"""
    kit = kit_crud.create_kit(db, kit_data)
    return kit


@router.put("/{kit_id}", response_model=KitResponse)
def update_kit(
    kit_id: int,
    kit_update: KitUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Update kit (Admin only)"""
    kit = kit_crud.update_kit(db, kit_id, kit_update)
    
    if not kit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kit not found"
        )
    
    return kit


@router.delete("/{kit_id}")
def delete_kit(
    kit_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Delete kit (Admin only)"""
    success = kit_crud.delete_kit(db, kit_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kit not found"
        )
    
    return {"message": "Kit deleted successfully"}


@router.patch("/{kit_id}/toggle-availability", response_model=KitResponse)
def toggle_kit_availability(
    kit_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Toggle kit availability (Admin only)"""
    kit = kit_crud.toggle_kit_availability(db, kit_id)
    
    if not kit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kit not found"
        )
    
    return kit
