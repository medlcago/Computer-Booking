from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BIGINT, String, CheckConstraint, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .booking import Booking
    from .payment import Payment
    from .ticket import Ticket


class User(Base):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    fullname: Mapped[str] = mapped_column(String(length=255))
    username: Mapped[str | None] = mapped_column(String(length=255))
    phone_number: Mapped[str] = mapped_column(String(length=255))
    password: Mapped[str] = mapped_column(String(length=255))
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_blocked: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    balance: Mapped[int] = mapped_column(CheckConstraint("balance >= 0"), default=0)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=text("TIMEZONE('utc', now())")
    )

    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    payments: Mapped[list["Payment"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, user_id={self.user_id!r}, username={self.username!r}, phone_number={self.phone_number!r}, balance={self.balance!r})"

    def __repr__(self):
        return str(self)
