from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BenefitBase(BaseModel):
    title: str
    description: str
    icon_emoji: Optional[str] = None
    display_order: Optional[int] = 0


class BenefitCreate(BenefitBase):
    pass


class BenefitUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon_emoji: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


class BenefitResponse(BenefitBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
