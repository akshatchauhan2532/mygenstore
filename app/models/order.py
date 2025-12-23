# app/orders/models.py
import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.base import Base
from enum import Enum


class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"),nullable=False,index=True)
    address_id = Column(UUID(as_uuid=True), ForeignKey("user_addresses.id", ondelete="RESTRICT"),nullable=False)

    total_amount = Column(Numeric(12, 2), nullable=False)
    status = Column(String, default=OrderStatus.pending.value, nullable=False)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="orders")
    address = relationship(
        "UserAddress",
        back_populates="orders"
    )
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    payments = relationship("Payment", back_populates="order")
    refunds = relationship("Refund", back_populates="order")
