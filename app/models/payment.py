from sqlalchemy import Column, String, ForeignKey, Numeric, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid 
from sqlalchemy.dialects.postgresql import UUID
from app.database.session import Base
from enum import Enum

class PaymentStatus(str, Enum):
    pending = "pending"
    succeeded = "succeeded"
    failed = "failed"
    refunded = "refunded"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="SET NULL"), nullable=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    stripe_session_id = Column(String, unique=True, index=True, nullable=False)
    stripe_payment_intent_id = Column(String, unique=True, index=True, nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="INR")
    status = Column(String, default="pending", nullable=False)
    payment_method = Column(String, nullable=True) 
    raw_response = Column(JSON, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="payments")
    order = relationship("Order", back_populates="payments")
    refunds = relationship("Refund", back_populates="payment")