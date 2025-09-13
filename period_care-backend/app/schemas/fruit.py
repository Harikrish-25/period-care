from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FruitBase(BaseModel):
    name: str
    price: float
    benefits: Optional[str] = None
    emoji_icon: Optional[str] = None


class FruitCreate(FruitBase):
    pass


class FruitUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    benefits: Optional[str] = None
    emoji_icon: Optional[str] = None
    is_available: Optional[bool] = None


class FruitResponse(FruitBase):
    id: int
    is_available: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class FruitList(BaseModel):
    id: int
    name: str
    price: float
    emoji_icon: Optional[str] = None
    is_available: bool
    
    class Config:
        from_attributes = True
