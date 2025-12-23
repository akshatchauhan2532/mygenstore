import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.base import Base
from enum import Enum 
class AddressType(str, Enum):
    home = "home"
    work = "work"
    other = "other"


class UserAddress(Base):
    __tablename__ = "user_addresses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True
    )

    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False, index=True)

    address_line1 = Column(String, nullable=False)
    address_line2 = Column(String)

    city = Column(String, nullable=False)
    pincode = Column(String, nullable=False)

    address_type = Column(
        String,
        default=AddressType.home.value,
        nullable=False
    )

    is_default = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    user = relationship("User", back_populates="addresses")
    orders = relationship("Order", back_populates="address")

    __table_args__ = (
        Index(
            "ix_user_default_address",
            "user_id",
            "is_default",
            unique=False
        ),
    )
