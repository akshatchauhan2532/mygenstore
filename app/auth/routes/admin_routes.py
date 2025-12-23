from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from fastapi_utils.cbv import cbv

from app.database.session import get_db
from app.auth.schemas import UserLogin, Token
from app.auth.services import get_user_by_email, verify_password, create_access_token
from app.auth.dependencies import require_roles

router = APIRouter(
    prefix="/auth/admin",
    tags=["Admin Auth"]
)

@cbv(router)
class AdminAuthRoutes:

    @router.post("/login", response_model=Token)
    async def login(
        self,
        user_in: UserLogin,
        response: Response,
        db: Session = Depends(get_db),
    ):
        user = await get_user_by_email(db, user_in.email)

        if (
            not user
            or not verify_password(user_in.password, user.password)
            or user.role.value != "admin"
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials or role",
            )

        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_access_token({"sub": str(user.id)})

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=7 * 24 * 60 * 60,
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    @router.get("/me")
    async def admin_profile(
        current_user=Depends(require_roles(["admin"]))
    ):
        return current_user
