from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BIGINT, ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .computer import Computer


class Booking(Base):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.user_id"))
    computer_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("computers.computer_id"))
    start_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    end_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

    user: Mapped["User"] = relationship(back_populates="bookings")
    computer: Mapped["Computer"] = relationship(back_populates="bookings")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, user_id={self.user_id!r}, computer_id={self.computer_id!r}, start_time={self.start_time!r}, end_time={self.end_time!r})"

    def __repr__(self):
        return str(self)
