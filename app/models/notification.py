import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database.base import Base

class NotificationType(PyEnum):
    order_confirmation = "order_confirmation"
    payment_success = "payment_success"
    payment_failed = "payment_failed"
    order_shipped = "order_shipped"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")
    messages = relationship("NotificationMessage", back_populates="notification")

class NotificationMessage(Base):
    __tablename__ = "notification_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    notification_id = Column(UUID(as_uuid=True), ForeignKey("notifications.id"), nullable=False)
    related_type = Column(String, nullable=True)
    related_id = Column(UUID(as_uuid=True), nullable=True)
    type = Column(Enum(NotificationType, name="notification_type"), nullable=False)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    notification = relationship("Notification", back_populates="messages")
