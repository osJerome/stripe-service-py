# FastAPI Stripe Payment Service

A robust FastAPI-based service for handling Stripe payments with proper error handling, webhook processing, and currency validation.

## Features

- 🔒 Secure payment processing
- 💳 Payment intent creation
- 🔄 Webhook handling
- 💱 Multi-currency support
- ✅ Amount validation
- 🚀 Asynchronous processing
- 📝 OpenAPI documentation

## Prerequisites

- Python 3.8+
- pip
- Stripe account
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fastapi-stripe-service
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```env
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

## Project Structure

```
stripe-service/
├── .env
├── .env.example
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── payment.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── payment_routes.py
│   └── services/
│       ├── __init__.py
│       └── stripe_service.py
└── tests/
    ├── __init__.py
    └── test_payment.py
```

## Running the Service

1. Start the development server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Create Payment Intent
```http
POST /api/payments/create-payment-intent
```

Request body:
```json
{
    "amount": 1000,
    "currency": "usd",
    "payment_method_types": ["card"],
    "description": "Payment for order #123"
}
```

Response:
```json
{
    "client_secret": "pi_xxx_secret_xxx",
    "payment_intent_id": "pi_xxx"
}
```

### Webhook Handler
```http
POST /api/payments/webhook
```

## Amount Validation

The service validates minimum amounts for different currencies:
- USD: $0.50 (50 cents)
- EUR: €0.50 (50 cents)
- SGD: S$0.50 (50 cents)

## Webhook Setup

### Local Development

1. Install Stripe CLI:
```bash
# macOS
brew install stripe/stripe-cli/stripe

# Windows
scoop install stripe
```

2. Login to Stripe:
```bash
stripe login
```

3. Forward webhooks:
```bash
stripe listen --forward-to localhost:8000/api/payments/webhook
```

### Production

1. Go to Stripe Dashboard → Developers → Webhooks
2. Add endpoint: `https://your-domain.com/api/payments/webhook`
3. Select events to listen for:
   - payment_intent.succeeded
   - payment_intent.payment_failed
   - charge.succeeded
   - charge.failed

## Error Handling

The service handles various error cases:
- Invalid currency
- Amount below minimum
- Cross-currency conversion issues
- Invalid webhook signatures
- General Stripe API errors

Example error response:
```json
{
    "detail": "Amount must be at least 0.50 USD. Provided amount: 0.10 USD"
}
```

## Frontend Integration

```javascript
const stripe = Stripe('your_publishable_key');

async function createPayment() {
    const response = await fetch('/api/payments/create-payment-intent', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            amount: 1000,
            currency: 'usd'
        }),
    });
    
    const { client_secret } = await response.json();
    
    const result = await stripe.confirmCardPayment(client_secret, {
        payment_method: {
            card: elements.getElement('card'),
            billing_details: {
                name: 'Customer Name'
            }
        }
    });
}
```

## Testing

Run tests:
```bash
pytest
```

## Deployment

1. Set environment variables
2. Configure CORS settings
3. Set up SSL/TLS
4. Configure webhook endpoints
5. Set up monitoring
6. Implement logging

## Security Considerations

- Use HTTPS in production
- Keep Stripe SDK updated
- Implement rate limiting
- Validate webhook signatures
- Handle errors gracefully
- Use environment variables for sensitive data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

[MIT License](LICENSE)
