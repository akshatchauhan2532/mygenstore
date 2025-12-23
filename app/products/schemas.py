from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from uuid import UUID

class ProductCreate(BaseModel):
    name:str
    description: Optional[str] = None
    price: float
    stock: Optional[int] = 0
    is_active: Optional[bool] = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None


class ProductOut(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)




