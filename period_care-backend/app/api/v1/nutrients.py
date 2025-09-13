from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.schemas.nutrient import NutrientResponse, NutrientCreate, NutrientUpdate, NutrientList
from app.crud import nutrient as nutrient_crud
from app.api.v1.auth import get_current_admin_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[NutrientList])
def get_all_nutrients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all available nutrients"""
    nutrients = nutrient_crud.get_nutrients(db, skip, limit, available_only=True)
    return nutrients


@router.get("/{nutrient_id}", response_model=NutrientResponse)
def get_nutrient_by_id(nutrient_id: int, db: Session = Depends(get_db)):
    """Get specific nutrient by ID"""
    nutrient = nutrient_crud.get_nutrient_by_id(db, nutrient_id)
    
    if not nutrient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nutrient not found"
        )
    
    return nutrient


@router.post("/", response_model=NutrientResponse)
def create_nutrient(
    nutrient_data: NutrientCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Create new nutrient (Admin only)"""
    nutrient = nutrient_crud.create_nutrient(db, nutrient_data)
    return nutrient


@router.put("/{nutrient_id}", response_model=NutrientResponse)
def update_nutrient(
    nutrient_id: int,
    nutrient_update: NutrientUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Update nutrient (Admin only)"""
    nutrient = nutrient_crud.update_nutrient(db, nutrient_id, nutrient_update)
    
    if not nutrient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nutrient not found"
        )
    
    return nutrient


@router.delete("/{nutrient_id}")
def delete_nutrient(
    nutrient_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Delete nutrient (Admin only)"""
    success = nutrient_crud.delete_nutrient(db, nutrient_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nutrient not found"
        )
    
    return {"message": "Nutrient deleted successfully"}


@router.patch("/{nutrient_id}/toggle-availability", response_model=NutrientResponse)
def toggle_nutrient_availability(
    nutrient_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Toggle nutrient availability (Admin only)"""
    nutrient = nutrient_crud.toggle_nutrient_availability(db, nutrient_id)
    
    if not nutrient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nutrient not found"
        )
    
    return nutrient
