import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from app.database.base import Base


class UserRole(PyEnum):
    user = "user"
    admin = "admin"
    superadmin = "superadmin"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=True)

    role = Column(Enum(UserRole, name="userrole"), default=UserRole.user)

    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False)

    provider = Column(String, default="local", index=True)
    provider_id = Column(String, nullable=True, index=True)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    addresses = relationship(
        "UserAddress",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    cart = relationship(
        "Cart",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    orders = relationship("Order", back_populates="user")
    payments = relationship("Payment", back_populates="user")