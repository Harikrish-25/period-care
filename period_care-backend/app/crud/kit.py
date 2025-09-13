from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.kit import Kit
from app.schemas.kit import KitCreate, KitUpdate


def get_kit_by_id(db: Session, kit_id: int) -> Optional[Kit]:
    return db.query(Kit).filter(Kit.id == kit_id).first()


def get_kits(db: Session, skip: int = 0, limit: int = 100, available_only: bool = True) -> List[Kit]:
    query = db.query(Kit)
    if available_only:
        query = query.filter(Kit.is_available == True)
    return query.offset(skip).limit(limit).all()


def get_kits_by_type(db: Session, kit_type: str) -> List[Kit]:
    return db.query(Kit).filter(Kit.type == kit_type, Kit.is_available == True).all()


def create_kit(db: Session, kit: KitCreate) -> Kit:
    db_kit = Kit(**kit.dict())
    db.add(db_kit)
    db.commit()
    db.refresh(db_kit)
    return db_kit


def update_kit(db: Session, kit_id: int, kit_update: KitUpdate) -> Optional[Kit]:
    db_kit = get_kit_by_id(db, kit_id)
    if not db_kit:
        return None
    
    update_data = kit_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_kit, field, value)
    
    db.commit()
    db.refresh(db_kit)
    return db_kit


def delete_kit(db: Session, kit_id: int) -> bool:
    db_kit = get_kit_by_id(db, kit_id)
    if not db_kit:
        return False
    
    db.delete(db_kit)
    db.commit()
    return True


def toggle_kit_availability(db: Session, kit_id: int) -> Optional[Kit]:
    db_kit = get_kit_by_id(db, kit_id)
    if not db_kit:
        return None
    
    db_kit.is_available = not db_kit.is_available
    db.commit()
    db.refresh(db_kit)
    return db_kit
