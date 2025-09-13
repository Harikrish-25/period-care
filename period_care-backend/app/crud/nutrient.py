from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.nutrient import Nutrient
from app.schemas.nutrient import NutrientCreate, NutrientUpdate


def get_nutrient_by_id(db: Session, nutrient_id: int) -> Optional[Nutrient]:
    return db.query(Nutrient).filter(Nutrient.id == nutrient_id).first()


def get_nutrients(db: Session, skip: int = 0, limit: int = 100, available_only: bool = True) -> List[Nutrient]:
    query = db.query(Nutrient)
    if available_only:
        query = query.filter(Nutrient.is_available == True)
    return query.offset(skip).limit(limit).all()


def create_nutrient(db: Session, nutrient: NutrientCreate) -> Nutrient:
    db_nutrient = Nutrient(**nutrient.dict())
    db.add(db_nutrient)
    db.commit()
    db.refresh(db_nutrient)
    return db_nutrient


def update_nutrient(db: Session, nutrient_id: int, nutrient_update: NutrientUpdate) -> Optional[Nutrient]:
    db_nutrient = get_nutrient_by_id(db, nutrient_id)
    if not db_nutrient:
        return None
    
    update_data = nutrient_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_nutrient, field, value)
    
    db.commit()
    db.refresh(db_nutrient)
    return db_nutrient


def delete_nutrient(db: Session, nutrient_id: int) -> bool:
    db_nutrient = get_nutrient_by_id(db, nutrient_id)
    if not db_nutrient:
        return False
    
    db.delete(db_nutrient)
    db.commit()
    return True


def toggle_nutrient_availability(db: Session, nutrient_id: int) -> Optional[Nutrient]:
    db_nutrient = get_nutrient_by_id(db, nutrient_id)
    if not db_nutrient:
        return None
    
    db_nutrient.is_available = not db_nutrient.is_available
    db.commit()
    db.refresh(db_nutrient)
    return db_nutrient
