from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.testimonial import Testimonial
from app.schemas.testimonial import TestimonialCreate, TestimonialUpdate


def get_testimonial_by_id(db: Session, testimonial_id: int) -> Optional[Testimonial]:
    return db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()


def get_testimonials(db: Session, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[Testimonial]:
    query = db.query(Testimonial)
    if active_only:
        query = query.filter(Testimonial.is_active == True)
    return query.order_by(Testimonial.rating.desc()).offset(skip).limit(limit).all()


def get_featured_testimonials(db: Session) -> List[Testimonial]:
    return db.query(Testimonial).filter(
        Testimonial.is_featured == True,
        Testimonial.is_active == True
    ).order_by(Testimonial.rating.desc()).all()


def create_testimonial(db: Session, testimonial: TestimonialCreate) -> Testimonial:
    db_testimonial = Testimonial(**testimonial.dict())
    db.add(db_testimonial)
    db.commit()
    db.refresh(db_testimonial)
    return db_testimonial


def update_testimonial(db: Session, testimonial_id: int, testimonial_update: TestimonialUpdate) -> Optional[Testimonial]:
    db_testimonial = get_testimonial_by_id(db, testimonial_id)
    if not db_testimonial:
        return None
    
    update_data = testimonial_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_testimonial, field, value)
    
    db.commit()
    db.refresh(db_testimonial)
    return db_testimonial


def delete_testimonial(db: Session, testimonial_id: int) -> bool:
    db_testimonial = get_testimonial_by_id(db, testimonial_id)
    if not db_testimonial:
        return False
    
    db.delete(db_testimonial)
    db.commit()
    return True
