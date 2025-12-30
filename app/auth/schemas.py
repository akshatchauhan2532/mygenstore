from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from uuid import UUID

# ---------------------------------------------------
# BASE SCHEMAS (Shared fields)
# ---------------------------------------------------
class UserBase(BaseModel):
    name: str
    email: EmailStr

# ---------------------------------------------------
# REQUEST SCHEMAS (Input)
# ---------------------------------------------------
class UserCreate(UserBase):
    """Used for standard registration - Password is STRICTLY REQUIRED"""
    password: str

class UserSocialCreate(UserBase):
    """Used internally for Google/OAuth logic - No password field exists here"""
    provider: str
    provider_id: str
    is_active: bool = True
    is_verified: bool = True  # Social providers verify email for us

class UserLogin(BaseModel):
    """Standard Login Request"""
    email: EmailStr
    password: str

# ---------------------------------------------------
# RESPONSE SCHEMAS (Output)
# ---------------------------------------------------
class UserOut(UserBase):
    """Standard User Response - Always hide the password/sensitive data"""
    id: UUID
    is_active: bool
    role: str
    provider: str

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    """JWT Token Response"""
    access_token: str
    token_type: str = "bearer"

class GoogleTokenRequest(BaseModel):
    """Schema to receive the ID token from frontend if using a popup flow"""
    id_token: str