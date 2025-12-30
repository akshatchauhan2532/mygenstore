from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.auth.schemas import UserCreate, UserOut, Token, UserLogin , UserSocialCreate
from app.auth.services import create_user, get_user_by_id, verify_password, create_access_token, create_refresh_token,get_user_by_email
from app.auth.dependencies import get_current_active_user
from app.models.user import User
from app.core.config import settings
import httpx
from urllib.parse import urlencode




router = APIRouter(prefix="/auth/user", tags=["User Auth"])

@cbv(router)
class UserAuthRoutes:
    db: AsyncSession = Depends(get_db)  # async session

    # ----------------------- Existing Routes -----------------------
    @router.post("/register", response_model=UserOut)
    async def register(self, user_in: UserCreate):
        user = await get_user_by_email(self.db, user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        return await create_user(self.db, user_in)

    @router.post("/login", response_model=Token)
    async def login(self, user_in: UserLogin, response: Response):
        user = await get_user_by_email(self.db, user_in.email)
        if not user or not verify_password(user_in.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=7*24*60*60
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @router.get("/me", response_model=UserOut)
    async def me(self, current_user: User = Depends(get_current_active_user)):
        return current_user

    # ----------------------- Google OAuth2 Routes -----------------------
    @router.get("/google/login")
    async def google_login(self):
        # Build Google OAuth2 URL
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent"
        }
        url = settings.GOOGLE_AUTH_URL + "?" + urlencode(params)
        return {"auth_url": url}

    @router.get("/google/callback", response_model=Token)
    async def google_callback(self, code: str, response: Response):
        # Exchange code for Google access token
        async with httpx.AsyncClient() as client:
            token_res = await client.post(settings.GOOGLE_TOKEN_URL, data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            })
            token_res = token_res.json()

        access_token_google = token_res.get("access_token")
        if not access_token_google:
            raise HTTPException(status_code=400, detail="Failed to get Google access token")

        # Fetch user info from Google
        async with httpx.AsyncClient() as client:
            user_info_res = await client.get(settings.GOOGLE_USERINFO_URL, headers={
                "Authorization": f"Bearer {access_token_google}"
            })
            user_info = user_info_res.json()

        email = user_info.get("email")
        name = user_info.get("name")
        google_id = user_info.get("sub")

        if not email:
            raise HTTPException(status_code=400, detail="Google account has no email")

        # Check local DB
        user = await get_user_by_email(self.db, email)
        if not user:
            # Create new user for first-time Google login
            user = await create_user(self.db, UserSocialCreate(
                email=email,
                name=name,
                password=None,  # No password for Google users
                provider="google",
                provider_id=google_id
            ))

        # Issue local JWT tokens
        role_value = user.role.value if hasattr(user.role, "value") else user.role
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_refresh_token({"sub": str(user.id)})

        # Set refresh token cookie
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=7*24*60*60
        )

        return {"access_token": access_token, "token_type": "bearer"}
