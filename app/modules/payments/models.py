from enum import Enum
from uuid import UUID

from sqlalchemy import Boolean, Enum as SQLEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.database import BaseEntity


class PaymentStatus(str, Enum):
    CREATED = "created"
    PAID = "paid"
    FAILED = "failed"


class Payment(BaseEntity):
    __tablename__ = "payments"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    razorpay_order_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    razorpay_payment_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    amount: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="INR",
    )

    status: Mapped[PaymentStatus] = mapped_column(
        SQLEnum(PaymentStatus),
        default=PaymentStatus.CREATED,
    )

    verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )