from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date


class ReminderBase(BaseModel):
    user_id: int
    reminder_type: str = "monthly_reorder"
    last_order_date: date


class ReminderCreate(ReminderBase):
    pass


class ReminderUpdate(BaseModel):
    status: Optional[str] = None
    admin_notified: Optional[bool] = None


class ReminderResponse(ReminderBase):
    id: int
    reminder_date: Optional[datetime] = None
    status: str
    admin_notified: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ReminderWithUser(BaseModel):
    id: int
    user_id: int
    user_name: str
    user_email: str
    user_mobile: str
    reminder_type: str
    last_order_date: date
    reminder_date: Optional[datetime] = None
    status: str
    admin_notified: bool
    
    class Config:
        from_attributes = True
