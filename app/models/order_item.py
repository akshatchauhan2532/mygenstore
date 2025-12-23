# app/orders/models.py
from sqlalchemy import Column, Integer, ForeignKey, Numeric,String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from app.database.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id", ondelete="CASCADE"),nullable=False, index=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id",ondelete="RESTRICT"),nullable=False)

    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")