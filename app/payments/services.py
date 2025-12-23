from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select, and_
from app.models.payment import Payment, PaymentStatus
from app.models.order import Order, OrderStatus
from uuid import UUID
from typing import List
import logging

logger = logging.getLogger(__name__)

async def create_payment_entry(db: AsyncSession, order_id: UUID, user_id: UUID, amount: float, session_id: str):
    new_payment = Payment(
        order_id=order_id,
        user_id=user_id,
        amount=amount,
        stripe_session_id=session_id,
        status=PaymentStatus.pending.value
    )
    db.add(new_payment)
    await db.commit()
    await db.refresh(new_payment)
    return new_payment

async def mark_payment_as_success(db: AsyncSession, order_id: str, raw_data: dict):
    try:
        order_uuid = UUID(order_id)
        # Stripe webhooks wrap the session object inside data -> object
        stripe_obj = raw_data.get("data", {}).get("object", {})
        
        session_id = stripe_obj.get("id") # This is the cs_test_... ID
        payment_intent = stripe_obj.get("payment_intent") # This is the pi_... ID

        await db.execute(
            update(Payment)
            .where(Payment.order_id == order_uuid)
            .where(Payment.stripe_session_id == session_id)
            .values(
                status=PaymentStatus.succeeded.value,
                stripe_payment_intent_id=payment_intent,
                payment_method=stripe_obj.get("payment_method_types", ["card"])[0],
                raw_response=raw_data
            )
        )
        
        await db.execute(
            update(Order)
            .where(Order.id == order_uuid)
            .values(status=OrderStatus.paid.value)
        )
        
        await db.commit()
        logger.info(f"AUDIT: Order {order_id} successfully paid. Stripe Session: {session_id}")
        
    except Exception as e:
        await db.rollback()
        logger.error(f"AUDIT_FAILURE: Payment update failed for order {order_id}: {str(e)}")
        raise e

async def get_order_for_payment(db: AsyncSession, order_id: UUID, user_id: UUID):
    result = await db.execute(select(Order).where(and_(Order.id == order_id, Order.user_id == user_id)))
    return result.scalars().first()

async def get_user_payment_history(db: AsyncSession, user_id: UUID) -> List[Payment]:
    result = await db.execute(
        select(Payment)
        .where(Payment.user_id == user_id)
        .order_by(Payment.created_at.desc())
    )
    return result.scalars().all()

async def get_payment_by_order(db: AsyncSession, order_id: UUID, user_id: UUID):
    result = await db.execute(select(Payment).where(and_(Payment.order_id == order_id, Payment.user_id == user_id)))
    return result.scalars().first()