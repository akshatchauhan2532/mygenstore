from fastapi import APIRouter, Depends, HTTPException, Body, status, Request
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from app.auth.dependencies import require_roles
from app.database.session import get_db
from app.payments.stripe import StripeService
from app.payments import services, schemas
from app.models.order import OrderStatus
import stripe
from app.core.config import settings

router = APIRouter(prefix="/payments", tags=["Payments"])

@cbv(router)
class PaymentCBV:
    db: AsyncSession = Depends(get_db)

    @router.post("/checkout/{order_id}", response_model=schemas.CheckoutResponse)
    async def create_checkout(self, order_id: UUID, current_user=Depends(require_roles(["user"]))):
        order = await services.get_order_for_payment(self.db, order_id, current_user.id)

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Order not found or access denied."
            )
        
        if order.status == OrderStatus.paid.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="This order has already been paid."
            )

        try:
            session = StripeService.create_checkout_session(
                order_id=order.id,
                amount=float(order.total_amount),
                user_email=current_user.email
            )
            
            await services.create_payment_entry(
                db=self.db,
                order_id=order.id,
                user_id=current_user.id,
                amount=order.total_amount,
                session_id=session.id
            )
            
            return {"checkout_url": session.url}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/history", response_model=List[schemas.PaymentOut])
    async def get_my_payments(self, current_user=Depends(require_roles(["user"]))):
        return await services.get_user_payment_history(self.db, current_user.id)

    @router.get("/status/{order_id}", response_model=schemas.PaymentOut)
    async def get_payment_status(self, order_id: UUID, current_user=Depends(require_roles(["user"]))):
        payment = await services.get_payment_by_order(self.db, order_id, current_user.id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment record not found")
        return payment

    @router.post("/webhook", include_in_schema=False)
    async def stripe_webhook(self, request: Request):
        payload = await request.body()
        sig_header = request.headers.get("stripe-signature")

        if not sig_header:
            raise HTTPException(status_code=400, detail="Missing Stripe signature")

        try:
            # Verifies that the event actually came from Stripe
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            raise HTTPException(status_code=400, detail="Invalid signature")

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            
            # Pulling the UUID we attached in StripeService
            order_id = session.get("metadata", {}).get("order_id")

            if order_id:
                # Check if order is already processed to prevent duplicate logic
                order = await services.get_order_by_id(self.db, order_id)
                if order and order.status == OrderStatus.paid.value:
                    return {"status": "already_processed"}

                # Standardizing the success update
                await services.mark_payment_as_success(
                    db=self.db,
                    order_id=order_id,
                    raw_data=event
                )

        return {"status": "ok"}