from fastapi import APIRouter, Header, Request
from ..services.stripe_service import StripeService
from ..models.payment import PaymentIntent, PaymentResponse

router = APIRouter()

@router.post("/create-payment-intent", response_model=PaymentResponse)
async def create_payment_intent(payment: PaymentIntent):
    return await StripeService.create_payment_intent(payment)

@router.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()
    event = await StripeService.handle_webhook(payload, stripe_signature)
    
    # Handle different event types
    if event.type == "payment_intent.succeeded":
        payment_intent = event.data.object
        # Handle successful payment
        print(f"Payment succeeded: {payment_intent.id}")
    
    return {"status": "success"}