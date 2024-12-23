from fastapi import FastAPI
from .routes import payment_routes
from .config import get_settings

app = FastAPI(title="Stripe Payment Service")
settings = get_settings()

app.include_router(payment_routes.router, prefix="/api/payments", tags=["payments"])

@app.get("/", tags=["root"])
async def root():
    return {"message": "Stripe Payment Service is running"}