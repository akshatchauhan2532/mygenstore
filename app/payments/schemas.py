from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal

class PaymentBase(BaseModel):
    amount: Decimal
    currency: str = "INR"

class CheckoutResponse(BaseModel):
    """The response for Step 1: Redirecting to Stripe"""
    checkout_url: str

class PaymentOut(PaymentBase):
    """The response for Step 3: Getting payment details from DB"""
    id: UUID
    order_id: Optional[UUID]
    user_id: Optional[UUID]
    status: str
    stripe_session_id: str
    stripe_payment_intent_id: Optional[str] = None
    payment_method: Optional[str] = None
    created_at: datetime
    
    # Updated for Pydantic V2 (formerly class Config)
    model_config = ConfigDict(from_attributes=True)

class WebhookPayload(BaseModel):
    """Used for Postman simulation and data validation"""
    type: str
    data: Dict[str, Any]