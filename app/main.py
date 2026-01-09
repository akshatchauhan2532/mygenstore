from fastapi import FastAPI,HTTPException


from app.auth.routes import router as auth_router
from app.auth.routes import router as superadmin_router
from app.products.routes import router as products_router
from app.cart.routes import router as cart_router
from app.address.routes import router as address_router
from app.orders.routes import router as order_router
from app.payments.routes import router as payment_routes
from app.auth.routes.refresh_routes import router as refresh_router

import os 
from redis import asyncio as aioredis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
app = FastAPI(title="MyGenStore API")


CUSTOM_LIMITS = {
    "/v1/api/auth/login": {"times": 5, "seconds": 60},
    "/v1/api/auth/register": {"times": 3, "seconds": 3600},
    "/v1/api/payments/place-order": {"times": 5, "seconds": 60},
}
DEFAULT_LIMIT = {"times": 60, "seconds": 60}

async def service_identifier(request: Request):
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]
    return request.client.host

@app.on_event("startup")
async def startup():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    redis = aioredis.from_url(redis_url, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis, identifier=service_identifier)

@app.middleware("http")
async def global_rate_limit_middleware(request: Request, call_next):
    path = request.url.path
    policy = CUSTOM_LIMITS.get(path, DEFAULT_LIMIT)
    
    limiter = RateLimiter(times=policy["times"], seconds=policy["seconds"])
    try:
        await limiter(request, None)
    except HTTPException:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests. Please try again later."}
        )
            
    return await call_next(request)


class SimpleTimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        import time
        start_time = time.time()
        response: Response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SimpleTimingMiddleware)

app.include_router(auth_router, prefix="/v1/api")
app.include_router(superadmin_router, prefix="/v1/api")
app.include_router(products_router, prefix="/v1/api")
app.include_router(cart_router, prefix="/v1/api")
app.include_router(address_router, prefix="/v1/api")
app.include_router(order_router,prefix="/v1/api")
app.include_router(payment_routes,prefix="/v1/api")
app.include_router(refresh_router,prefix="/v1/api")