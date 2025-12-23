from pydantic import BaseModel, UUID4
from typing import List
from decimal import Decimal
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


class PlaceOrderIn(BaseModel):
    address_id: UUID4


class OrderItemOut(BaseModel):
    product_id: UUID4
    product_name: str
    quantity: int
    price_at_purchase: Decimal

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: UUID4
    total_amount: Decimal
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes=True


class OrderListOut(BaseModel):
    id: UUID4
    total_amount: Decimal
    status: OrderStatus
    created_at: datetime

    class Config:
        from_attributes = True
