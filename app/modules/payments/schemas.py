from pydantic import BaseModel, Field

from app.modules.payments.models import PaymentStatus


class CreateOrderRequest(BaseModel):
    amount: int = Field(..., gt=0)
    currency: str = "INR"


class CreateOrderResponse(BaseModel):
    order_id: str
    amount: int
    currency: str
    key: str


class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class PaymentResponse(BaseModel):
    order_id: str
    payment_id: str | None
    amount: int
    currency: str
    status: PaymentStatus
    verified: bool

    model_config = {
        "from_attributes": True
    }