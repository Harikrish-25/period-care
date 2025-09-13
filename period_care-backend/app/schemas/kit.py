from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class KitBase(BaseModel):
    name: str
    type: str  # basic, medium, premium
    base_price: float
    image_url: Optional[str] = None
    included_items: str  # JSON string
    description: Optional[str] = None


class KitCreate(KitBase):
    pass


class KitUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    base_price: Optional[float] = None
    image_url: Optional[str] = None
    included_items: Optional[str] = None
    description: Optional[str] = None
    is_available: Optional[bool] = None


class KitResponse(KitBase):
    id: int
    is_available: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class KitList(BaseModel):
    id: int
    name: str
    type: str
    base_price: float
    image_url: Optional[str] = None
    description: Optional[str] = None
    is_available: bool
    
    class Config:
        from_attributes = True
