from pydantic import BaseModel
from typing import Optional, List

class PaymentIntent(BaseModel):
    amount: int
    currency: str = "usd"
    payment_method_types: List[str] = ["card"]
    description: Optional[str] = None

class PaymentResponse(BaseModel):
    client_secret: str
    payment_intent_id: str