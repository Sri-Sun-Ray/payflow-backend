import json

from fastapi import HTTPException, status
from razorpay.errors import SignatureVerificationError

from app.core.config import settings
from app.core.razorpay_client import razorpay_client
from app.modules.payments.models import Payment, PaymentStatus
from app.modules.payments.repository import PaymentRepository


class PaymentService:

    def __init__(self, db):
        self.repository = PaymentRepository(db)

    async def create_order(
        self,
        user_id,
        amount: int,
        currency: str = "INR",
    ):

        razorpay_order = razorpay_client.order.create(
            {
                "amount": amount * 100,
                "currency": currency,
                "payment_capture": 1,
            }
        )

        payment = Payment(
            user_id=user_id,
            razorpay_order_id=razorpay_order["id"],
            amount=amount,
            currency=currency,
        )

        await self.repository.create_payment(payment)

        return {
            "order_id": razorpay_order["id"],
            "amount": amount,
            "currency": currency,
            "key": settings.RAZORPAY_KEY_ID,
        }

    def _to_response(self, payment: Payment) -> dict:
        return {
            "order_id": payment.razorpay_order_id,
            "payment_id": payment.razorpay_payment_id,
            "amount": payment.amount,
            "currency": payment.currency,
            "status": payment.status,
            "verified": payment.verified,
        }

    async def verify_payment(
        self,
        user_id,
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str,
    ):
        payment = await self.repository.get_by_order_id(razorpay_order_id)

        if payment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found",
            )

        if payment.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This order does not belong to you",
            )

        try:
            razorpay_client.utility.verify_payment_signature(
                {
                    "razorpay_order_id": razorpay_order_id,
                    "razorpay_payment_id": razorpay_payment_id,
                    "razorpay_signature": razorpay_signature,
                }
            )
        except SignatureVerificationError:
            payment = await self.repository.update_payment(
                payment,
                status=PaymentStatus.FAILED,
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment verification failed",
            )

        payment = await self.repository.update_payment(
            payment,
            razorpay_payment_id=razorpay_payment_id,
            status=PaymentStatus.PAID,
            verified=True,
        )

        return self._to_response(payment)

    async def handle_webhook(self, raw_body: bytes, signature: str):
        try:
            razorpay_client.utility.verify_webhook_signature(
                raw_body.decode(),
                signature,
                settings.RAZORPAY_WEBHOOK_SECRET,
            )
        except SignatureVerificationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid webhook signature",
            )

        event = json.loads(raw_body)
        event_type = event.get("event")

        if event_type not in ("payment.captured", "payment.failed"):
            return {"status": "ignored"}

        payment_entity = event["payload"]["payment"]["entity"]
        razorpay_order_id = payment_entity["order_id"]

        payment = await self.repository.get_by_order_id(razorpay_order_id)

        if payment is None:
            return {"status": "ignored"}

        if event_type == "payment.captured":
            await self.repository.update_payment(
                payment,
                razorpay_payment_id=payment_entity["id"],
                status=PaymentStatus.PAID,
                verified=True,
            )
        else:
            await self.repository.update_payment(
                payment,
                status=PaymentStatus.FAILED,
            )

        return {"status": "ok"}