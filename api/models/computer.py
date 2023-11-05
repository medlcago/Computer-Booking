from typing import TYPE_CHECKING

from sqlalchemy import String, BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .booking import Booking


class Computer(Base):
    computer_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    brand: Mapped[str] = mapped_column(String(length=255))
    model: Mapped[str] = mapped_column(String(length=255))
    cpu: Mapped[str] = mapped_column(String(length=255))
    ram: Mapped[int]
    storage: Mapped[int]
    gpu: Mapped[str] = mapped_column(String(length=255))
    description: Mapped[str | None] = mapped_column(String(length=255), default=None)
    category: Mapped[str] = mapped_column(String(length=255))
    price_per_hour: Mapped[int] = mapped_column(nullable=False)
    is_reserved: Mapped[bool] = mapped_column(default=False)

    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="computer",
        cascade="all, delete-orphan")

    def __str__(self):
        return f"{self.__class__.__name__}(computer_id={self.computer_id}, category={self.category!r}, price_per_hour={self.price_per_hour!r}, is_reserved={self.is_reserved!r})"

    def __repr__(self):
        return str(self)