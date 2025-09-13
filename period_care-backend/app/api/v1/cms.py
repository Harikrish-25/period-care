from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.config.database import get_db
from app.schemas.benefit import BenefitResponse, BenefitCreate, BenefitUpdate
from app.schemas.testimonial import TestimonialResponse, TestimonialCreate, TestimonialUpdate
from app.crud import benefit as benefit_crud, testimonial as testimonial_crud
from app.api.v1.auth import get_current_admin_user
from app.models.user import User

router = APIRouter()


# Benefits endpoints
@router.get("/benefits", response_model=List[BenefitResponse])
def get_benefits(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all active benefits"""
    benefits = benefit_crud.get_benefits(db, skip, limit, active_only=True)
    return benefits


@router.post("/benefits", response_model=BenefitResponse)
def create_benefit(
    benefit_data: BenefitCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Create new benefit (Admin only)"""
    benefit = benefit_crud.create_benefit(db, benefit_data)
    return benefit


@router.put("/benefits/{benefit_id}", response_model=BenefitResponse)
def update_benefit(
    benefit_id: int,
    benefit_update: BenefitUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Update benefit (Admin only)"""
    benefit = benefit_crud.update_benefit(db, benefit_id, benefit_update)
    
    if not benefit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Benefit not found"
        )
    
    return benefit


@router.delete("/benefits/{benefit_id}")
def delete_benefit(
    benefit_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Delete benefit (Admin only)"""
    success = benefit_crud.delete_benefit(db, benefit_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Benefit not found"
        )
    
    return {"message": "Benefit deleted successfully"}


# Testimonials endpoints
@router.get("/testimonials", response_model=List[TestimonialResponse])
def get_testimonials(
    skip: int = 0,
    limit: int = 100,
    featured_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get testimonials"""
    if featured_only:
        testimonials = testimonial_crud.get_featured_testimonials(db)
    else:
        testimonials = testimonial_crud.get_testimonials(db, skip, limit, active_only=True)
    
    return testimonials


@router.post("/testimonials", response_model=TestimonialResponse)
def create_testimonial(
    testimonial_data: TestimonialCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Create new testimonial (Admin only)"""
    testimonial = testimonial_crud.create_testimonial(db, testimonial_data)
    return testimonial


@router.put("/testimonials/{testimonial_id}", response_model=TestimonialResponse)
def update_testimonial(
    testimonial_id: int,
    testimonial_update: TestimonialUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Update testimonial (Admin only)"""
    testimonial = testimonial_crud.update_testimonial(db, testimonial_id, testimonial_update)
    
    if not testimonial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Testimonial not found"
        )
    
    return testimonial


@router.delete("/testimonials/{testimonial_id}")
def delete_testimonial(
    testimonial_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin_user)
):
    """Delete testimonial (Admin only)"""
    success = testimonial_crud.delete_testimonial(db, testimonial_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Testimonial not found"
        )
    
    return {"message": "Testimonial deleted successfully"}
