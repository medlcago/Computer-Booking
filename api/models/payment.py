from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BIGINT, ForeignKey, String, TIMESTAMP, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Payment(Base):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.user_id"))
    amount: Mapped[int]
    payload: Mapped[str | None] = mapped_column(String(length=255))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('utc', now())")
    )

    user: Mapped["User"] = relationship(back_populates="payments")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, user_id={self.user_id!r}, amount={self.amount!r}, payload={self.payload!r}, created_at={self.created_at!r})"

    def __repr__(self):
        return str(self)
