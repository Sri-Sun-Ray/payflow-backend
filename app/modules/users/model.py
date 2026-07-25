from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.common.database import BaseEntity

class User(BaseEntity):

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
    )