from fastapi import FastAPI


from app.auth.routes import router as auth_router
from app.auth.routes import router as superadmin_router
from app.products.routes import router as products_router
from app.cart.routes import router as cart_router
from app.address.routes import router as address_router
from app.orders.routes import router as order_router
from app.payments.routes import router as payment_routes


from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
app = FastAPI(title="MyGenStore API")

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