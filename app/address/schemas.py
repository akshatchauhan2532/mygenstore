from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime
from enum import Enum


class AddressType(str, Enum):
    home = "home"
    work = "work"
    other = "other"


class AddressCreate(BaseModel):
    full_name: str
    phone: str
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    pincode: str
    address_type: AddressType = AddressType.home
    is_default: bool = False

    model_config = ConfigDict(from_attributes=True)


class AddressUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    address_type: Optional[AddressType] = None
    is_default: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class AddressOut(BaseModel):
    id: UUID
    full_name: str
    phone: str
    address_line1: str
    address_line2: Optional[str]
    city: str
    pincode: str
    address_type: AddressType
    is_default: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AddressListOut(BaseModel):
    id: UUID
    address_line1: str
    city: str
    pincode: str
    is_default: bool

    model_config = ConfigDict(from_attributes=True)
