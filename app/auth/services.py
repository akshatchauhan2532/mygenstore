from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.models.user import User, UserRole
from app.auth.schemas import UserCreate,UserOut,UserSocialCreate
from app.core.config import settings
from uuid import UUID 
from typing import Union, Optional
# -------------------------
# CONFIG
# -------------------------

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -------------------------
# PASSWORD UTILS
# -------------------------

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

# -------------------------
# DATABASE OPERATIONS (ASYNC)
# -------------------------

async def get_user_by_id(db: AsyncSession, user_id: UUID):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email:str):
    stmt = select(User).where(User.email ==email)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_user_by_role(db: AsyncSession, role:str):
    stmt = select(User).where(User.role ==role)
    result = await db.execute(stmt)
    return result.scalars().first()


async def create_user(
    db: AsyncSession, 
    user_in: Union[UserCreate, UserSocialCreate], 
    role: UserRole = UserRole.user
) -> UserOut:
    user_data = user_in.model_dump()
    
    if isinstance(user_in, UserCreate):
        user_data["password"] = hash_password(user_in.password)
        user_data["provider"] = "local"
        user_data["is_verified"] = False
    else:
        user_data["password"] = None
        user_data["is_verified"] = True

    user_data["role"] = role
    user_data["is_active"] = True

    new_user = User(**user_data)
    db.add(new_user)
    
    try:
        await db.commit()
        await db.refresh(new_user)
    except Exception as e:
        await db.rollback()
        raise e

    return UserOut.model_validate(new_user)

# -------------------------
# JWT TOKEN
# -------------------------

def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)

    payload.update({
        "exp": expire,
        "type": "access"
    })

    encoded_jwt = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: int = 60*24*7*60):  # 7 days in minutes
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    payload.update({
        "exp": expire,
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt



def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "access":
            return None

        return payload.get("sub")
    except JWTError:
        return None


async def update_user_password(
    db: AsyncSession,
    email: str,
    new_password: str
):
    user = await get_user_by_email(db, email)
    if not user:
        return False

    user.password = hash_password(new_password)
    await db.commit()
    return True
