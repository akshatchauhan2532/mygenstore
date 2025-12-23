from fastapi import APIRouter
from .user_routes import router as user_router
from .admin_routes import router as admin_router
from .superadmin_routes import router as superadmin_router

router = APIRouter()
router.include_router(user_router)
router.include_router(admin_router)
router.include_router(superadmin_router)
