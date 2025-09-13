from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.benefit import Benefit
from app.schemas.benefit import BenefitCreate, BenefitUpdate


def get_benefit_by_id(db: Session, benefit_id: int) -> Optional[Benefit]:
    return db.query(Benefit).filter(Benefit.id == benefit_id).first()


def get_benefits(db: Session, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[Benefit]:
    query = db.query(Benefit)
    if active_only:
        query = query.filter(Benefit.is_active == True)
    return query.order_by(Benefit.display_order).offset(skip).limit(limit).all()


def create_benefit(db: Session, benefit: BenefitCreate) -> Benefit:
    db_benefit = Benefit(**benefit.dict())
    db.add(db_benefit)
    db.commit()
    db.refresh(db_benefit)
    return db_benefit


def update_benefit(db: Session, benefit_id: int, benefit_update: BenefitUpdate) -> Optional[Benefit]:
    db_benefit = get_benefit_by_id(db, benefit_id)
    if not db_benefit:
        return None
    
    update_data = benefit_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_benefit, field, value)
    
    db.commit()
    db.refresh(db_benefit)
    return db_benefit


def delete_benefit(db: Session, benefit_id: int) -> bool:
    db_benefit = get_benefit_by_id(db, benefit_id)
    if not db_benefit:
        return False
    
    db.delete(db_benefit)
    db.commit()
    return True
