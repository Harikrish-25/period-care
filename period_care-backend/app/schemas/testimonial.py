from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TestimonialBase(BaseModel):
    name: str
    rating: int  # 1-5
    testimonial_text: str
    location: Optional[str] = None


class TestimonialCreate(TestimonialBase):
    pass


class TestimonialUpdate(BaseModel):
    name: Optional[str] = None
    rating: Optional[int] = None
    testimonial_text: Optional[str] = None
    location: Optional[str] = None
    is_featured: Optional[bool] = None
    is_active: Optional[bool] = None


class TestimonialResponse(TestimonialBase):
    id: int
    is_featured: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
