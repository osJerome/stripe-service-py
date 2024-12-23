import stripe
from fastapi import HTTPException
from ..config import get_settings
from ..models.payment import PaymentIntent

settings = get_settings()
stripe.api_key = settings.stripe_secret_key

class StripeService:
    # Minimum amounts in cents for different currencies
    MINIMUM_AMOUNTS = {
        'usd': 50,    # $0.50 USD
        'sgd': 50,    # $0.50 SGD
        'eur': 50,    # €0.50 EUR
        # Add other currencies as needed
    }

    @staticmethod
    def validate_amount(amount: int, currency: str):
        currency = currency.lower()
        min_amount = StripeService.MINIMUM_AMOUNTS.get(currency)
        
        if min_amount is None:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported currency: {currency}"
            )
            
        if amount < min_amount:
            raise HTTPException(
                status_code=400,
                detail=f"Amount must be at least {min_amount/100:.2f} {currency.upper()}. "
                      f"Provided amount: {amount/100:.2f} {currency.upper()}"
            )

    @staticmethod
    async def create_payment_intent(payment: PaymentIntent):
        try:
            # Validate minimum amount before creating payment intent
            StripeService.validate_amount(payment.amount, payment.currency)
            
            intent = stripe.PaymentIntent.create(
                amount=payment.amount,
                currency=payment.currency,
                payment_method_types=payment.payment_method_types,
                description=payment.description
            )
            return {
                "client_secret": intent.client_secret,
                "payment_intent_id": intent.id
            }
        except stripe.error.InvalidRequestError as e:
            if "Amount must convert to at least" in str(e):
                # Handle cross-currency minimum amount errors
                raise HTTPException(
                    status_code=400,
                    detail=f"Payment amount too low: {str(e)}"
                )
            raise HTTPException(status_code=400, detail=str(e))
        except stripe.error.StripeError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def handle_webhook(payload: bytes, signature: str):
        try:
            event = stripe.Webhook.construct_event(
                payload,
                signature,
                settings.stripe_webhook_secret
            )
            return event
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid signature")