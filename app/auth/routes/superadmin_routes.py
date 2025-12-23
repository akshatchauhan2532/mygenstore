from fastapi import APIRouter, Depends, HTTPException,Response, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.auth.schemas import UserCreate, Token,UserLogin,UserOut
from app.auth.services import get_user_by_email, verify_password, create_access_token,create_user
from app.models.user import User
from fastapi_utils.cbv import cbv
from app.auth.dependencies import get_current_active_user, require_roles
router = APIRouter(prefix="/auth/superadmin", tags=["SuperAdmin Auth"])

@cbv(router)
class SuperAdminAuth:

    @router.post("/login", response_model=Token)
    async def login(self, user_in: UserLogin,response:Response, db: Session = Depends(get_db)):
        user = await get_user_by_email(db, user_in.email)
        if (
            not user 
            or not verify_password(user_in.password, user.password)
            or (hasattr(user, "role") and user.role.value != "superadmin") 
        ):
            raise HTTPException(status_code=401, detail="Invalid credentials or role")
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token = create_access_token({"sub": str(user.id)})
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=7*24*60*60
        )

        return {"access_token": access_token, "token_type": "bearer"}
    

    @router.post("/create-admin",response_model = UserOut)
    async def create_admin(self, admin_in: UserCreate, db: Session = Depends(get_db),user = Depends(require_roles(["superadmin"]))):
        exisiting_user = await get_user_by_email(db, admin_in.email)
        if exisiting_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        new_admin = await create_user(db, admin_in, role="admin")
        return new_admin
    
    @router.get("/me")
    async def superadmin_profile(self, current_user=Depends(require_roles(["superadmin"]))):
        return current_user
