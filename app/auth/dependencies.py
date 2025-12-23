from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.auth.services import decode_access_token, get_user_by_id
from app.models.user import User
from typing import List

oauth2_scheme= OAuth2PasswordBearer(
    tokenUrl="/v1/api/auth/user/login"
)



# ---------------------------------------------------
# GET CURRENT USER (ASYNC)
# ---------------------------------------------------
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    user_id = decode_access_token(token)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = await get_user_by_id(db, user_id = user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return user



# ---------------------------------------------------
# GET CURRENT ACTIVE USER (ASYNC)
# ---------------------------------------------------
async def get_current_active_user(
    current_user=Depends(get_current_user),
):
    # You should have `is_active` column in User model
    if hasattr(current_user, "is_active") and not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    
    return current_user



def require_roles(allowed_roles: List[str]):
    async def role_checker(
        current_user: User = Depends(get_current_active_user)
    ):
        user_role = (
            current_user.role.value
            if hasattr(current_user.role, "value")
            else current_user.role
        )

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return role_checker