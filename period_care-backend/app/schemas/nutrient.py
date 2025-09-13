from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NutrientBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None


class NutrientCreate(NutrientBase):
    pass


class NutrientUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    is_available: Optional[bool] = None


class NutrientResponse(NutrientBase):
    id: int
    is_available: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class NutrientList(BaseModel):
    id: int
    name: str
    price: float
    is_available: bool
    
    class Config:
        from_attributes = True
