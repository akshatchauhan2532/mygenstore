from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi_utils.cbv import cbv
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.auth.schemas import Token
from app.auth.services import create_access_token, create_refresh_token, get_user_by_id
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["refresh"])


@cbv(router)
class RefreshRoutes:
    db: AsyncSession = Depends(get_db)

    @router.post("/refresh", response_model=Token)
    async def refresh_token(self, request: Request):
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token missing",
            )

        try:
            payload = jwt.decode(
                refresh_token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )

            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid refresh token")

            user = await get_user_by_id(self.db, user_id)
            if not user:
                raise HTTPException(status_code=401, detail="User not found")

            new_access = create_access_token({"sub": str(user.id)})
            new_refresh = create_refresh_token({"sub": str(user.id)})

            response = Token(
                access_token=new_access,
                token_type="bearer"
            )

            return response

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token",
            )
