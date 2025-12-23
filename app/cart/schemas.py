from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal
from typing import List


class AddToCartIn(BaseModel):
    product_id: UUID
    quantity: int = 1


class CartItemOut(BaseModel):
    product_id: UUID
    quantity: int
    price_at_add: Decimal

    class Config:
        from_attributes = True


class CartOut(BaseModel):
    id: UUID
    items: list[CartItemOut]

    class Config:
        from_attributes = True