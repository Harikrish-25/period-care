from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    kit_id = Column(Integer, ForeignKey("kits.id"), nullable=False)
    selected_fruits = Column(Text, nullable=True)  # JSON string of fruit IDs
    selected_nutrients = Column(Text, nullable=True)  # JSON string of nutrient IDs
    scheduled_date = Column(Date, nullable=False)
    delivery_address = Column(Text, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(20), default="pending")  # pending, completed, cancelled
    whatsapp_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="orders")
    kit = relationship("Kit", back_populates="orders")
