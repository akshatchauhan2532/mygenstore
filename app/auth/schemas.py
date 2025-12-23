from pydantic import BaseModel, EmailStr , ConfigDict
from typing import Optional

# Request models
class UserCreate(BaseModel):
    name:str
    email: EmailStr
    password: Optional[str] = None

# Response models
class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    is_active: bool
    role: str

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# JWT token response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

