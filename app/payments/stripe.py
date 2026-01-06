import stripe
import logging
from uuid import UUID
from app.core.config import settings

logger = logging.getLogger(__name__)
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
                            'name': 'Order Confirmation',
                            'description': f'Payment for Order ID: {order_id}'
                        },
                        'unit_amount': int(amount * 100), 
                    },
                    'quantity': 1,
                }],
                mode='payment',
                customer_email=user_email,
                success_url="http://localhost:8000/payments/success",
                cancel_url="http://localhost:8000/payments/cancel",
                metadata={"order_id": str(order_id)},
                payment_intent_data={"metadata": {"order_id": str(order_id)}}
            )
        except stripe.error.CardError as e:
            logger.error(f"Card declined: {e.user_message}")
            raise Exception(f"Payment failed: {e.user_message}")
        except stripe.error.RateLimitError:
            logger.error("Stripe API rate limit hit")
            raise Exception("Server is busy, please try again later")
        except stripe.error.InvalidRequestError as e:
            logger.error(f"Invalid parameters for Stripe: {str(e)}")
            raise Exception("Invalid payment request parameters")
        except stripe.error.StripeError as e:
            logger.error(f"Stripe System Error: {str(e)}")
            raise Exception("Payment gateway is currently unavailable")
        except Exception as e:
            logger.error(f"Unexpected error in StripeService: {str(e)}")
            raise Exception("An internal error occurred during checkout")

    @staticmethod
    def initiate_refund(payment_intent_id: str):
        try:
            return stripe.Refund.create(payment_intent=payment_intent_id)
        except stripe.error.InvalidRequestError as e:
            logger.error(f"Refund failed (Invalid ID): {str(e)}")
            raise Exception("Could not process refund: Invalid payment record")
        except stripe.error.StripeError as e:
            logger.error(f"Stripe Refund Error: {str(e)}")
            raise Exception("Refund failed due to a gateway error")