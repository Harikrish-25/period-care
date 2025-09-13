from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.fruit import Fruit
from app.schemas.fruit import FruitCreate, FruitUpdate


def get_fruit_by_id(db: Session, fruit_id: int) -> Optional[Fruit]:
    return db.query(Fruit).filter(Fruit.id == fruit_id).first()


def get_fruits(db: Session, skip: int = 0, limit: int = 100, available_only: bool = True) -> List[Fruit]:
    query = db.query(Fruit)
    if available_only:
        query = query.filter(Fruit.is_available == True)
    return query.offset(skip).limit(limit).all()


def create_fruit(db: Session, fruit: FruitCreate) -> Fruit:
    db_fruit = Fruit(**fruit.dict())
    db.add(db_fruit)
    db.commit()
    db.refresh(db_fruit)
    return db_fruit


def update_fruit(db: Session, fruit_id: int, fruit_update: FruitUpdate) -> Optional[Fruit]:
    db_fruit = get_fruit_by_id(db, fruit_id)
    if not db_fruit:
        return None
    
    update_data = fruit_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_fruit, field, value)
    
    db.commit()
    db.refresh(db_fruit)
    return db_fruit


def delete_fruit(db: Session, fruit_id: int) -> bool:
    db_fruit = get_fruit_by_id(db, fruit_id)
    if not db_fruit:
        return False
    
    db.delete(db_fruit)
    db.commit()
    return True


def toggle_fruit_availability(db: Session, fruit_id: int) -> Optional[Fruit]:
    db_fruit = get_fruit_by_id(db, fruit_id)
    if not db_fruit:
        return None
    
    db_fruit.is_available = not db_fruit.is_available
    db.commit()
    db.refresh(db_fruit)
    return db_fruit
