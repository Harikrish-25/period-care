from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


class OrderBase(BaseModel):
    kit_id: int
    selected_fruits: Optional[str] = None  # JSON string of fruit IDs
    selected_nutrients: Optional[str] = None  # JSON string of nutrient IDs
    scheduled_date: date
    delivery_address: str


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    scheduled_date: Optional[date] = None
    delivery_address: Optional[str] = None


class OrderResponse(OrderBase):
    id: int
    user_id: int
    total_amount: float
    status: str
    whatsapp_sent: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class OrderWithDetails(BaseModel):
    id: int
    user_id: int
    kit_id: int
    kit_name: str
    kit_type: str
    kit_base_price: float
    user_name: str
    user_email: str
    user_mobile: str
    selected_fruits: Optional[str] = None
    selected_nutrients: Optional[str] = None
    scheduled_date: date
    delivery_address: str
    total_amount: float
    status: str
    whatsapp_sent: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class OrderCalculation(BaseModel):
    kit_price: float
    fruits_total: float
    nutrients_total: float
    total_amount: float
    breakdown: dict
