import stripe
import os
from uuid import UUID
from dotenv import load_dotenv
import logging
from app.core.config import settings
logger = logging.getLogger(__name__)
load_dotenv()

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:
    @staticmethod
    def create_checkout_session(order_id: UUID, amount: float, user_email: str):
        try:
            return stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': f'Order Confirmation',
                            'description': f'Payment for Order ID: {order_id}'
                        },
                        'unit_amount': int(amount * 100), 
                    },
                    'quantity': 1,
                }],
                mode='payment',
                customer_email=user_email,
                # In production, these would be your frontend URLs
                success_url="http://localhost:8000/payments/success",
                cancel_url="http://localhost:8000/payments/cancel",
                metadata={"order_id": str(order_id)} 
            )
        except stripe.error.StripeError as e:
            logger.error(f"Stripe API Error: {str(e)}")
            raise Exception(f"Could not connect to Payment Gateway: {str(e)}")
        
    @staticmethod
    def initiate_refund(payment_intent_id: str):
        try:
            refund = stripe.Refund.create(
                payment_intent=payment_intent_id,
            )
            return refund
        except stripe.error.StripeError as e:
            raise Exception(f"Stripe Refund Error: {str(e)}")