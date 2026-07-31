from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.modules.payments.schemas import (
    CreateOrderRequest,
    CreateOrderResponse,
    PaymentResponse,
    VerifyPaymentRequest,
)
from app.modules.payments.service import PaymentService
from app.modules.users.model import User

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post("/create-order", response_model=CreateOrderResponse)
async def create_order(
    request: CreateOrderRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PaymentService(db)

    return await service.create_order(
        user_id=current_user.id,
        amount=request.amount,
        currency=request.currency,
    )


@router.post("/verify", response_model=PaymentResponse)
async def verify_payment(
    request: VerifyPaymentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = PaymentService(db)

    return await service.verify_payment(
        user_id=current_user.id,
        razorpay_order_id=request.razorpay_order_id,
        razorpay_payment_id=request.razorpay_payment_id,
        razorpay_signature=request.razorpay_signature,
    )


@router.post("/webhook")
async def razorpay_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
    x_razorpay_signature: str = Header(...),
):
    service = PaymentService(db)
    raw_body = await request.body()

    return await service.handle_webhook(raw_body, x_razorpay_signature)