from sqlalchemy import Column, String, ForeignKey, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database.base import Base

class Refund(Base):
    __tablename__ = "refunds"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    payment_id = Column(UUID(as_uuid=True), ForeignKey("payments.id", ondelete="CASCADE"), nullable=False)
    stripe_refund_id = Column(String, unique=True, nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String, default="pending") 
    fee_deducted = Column(Numeric(10, 2), default=0.00) 
    cancellation_reason = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ORM Relationships
    order = relationship("Order", back_populates="refunds")
    payment = relationship("Payment", back_populates="refunds")