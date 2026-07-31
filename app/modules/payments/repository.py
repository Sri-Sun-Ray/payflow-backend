from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.payments.models import Payment, PaymentStatus


class PaymentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_payment(self, payment: Payment):
        self.db.add(payment)
        await self.db.commit()
        await self.db.refresh(payment)
        return payment

    async def get_by_order_id(self, razorpay_order_id: str) -> Payment | None:
        result = await self.db.execute(
            select(Payment).where(Payment.razorpay_order_id == razorpay_order_id)
        )
        return result.scalar_one_or_none()

    async def update_payment(
        self,
        payment: Payment,
        *,
        razorpay_payment_id: str | None = None,
        status: PaymentStatus | None = None,
        verified: bool | None = None,
    ) -> Payment:
        if razorpay_payment_id is not None:
            payment.razorpay_payment_id = razorpay_payment_id
        if status is not None:
            payment.status = status
        if verified is not None:
            payment.verified = verified

        await self.db.commit()
        await self.db.refresh(payment)
        return payment