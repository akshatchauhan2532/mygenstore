from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.auth.schemas import UserCreate, UserOut, Token, UserLogin,token
from app.auth.services import create_user, get_user_by_id, verify_password, create_access_token, create_refresh_token,get_user_by_email
from app.auth.dependencies import get_current_active_user
from app.models.user import User
from app.core.config import settings
import httpx


router = APIRouter(prefix="/auth/refresh",tags=["refresh"])

@cbv(router)
class refresh_routes:
    @router.post("/new",response_model = token)
    def refresh():
        pass