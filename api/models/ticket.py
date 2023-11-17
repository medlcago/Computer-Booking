from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BIGINT, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from ..enums import TicketStatus

if TYPE_CHECKING:
    from .user import User


class Ticket(Base):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(length=255))
    status: Mapped[TicketStatus] = mapped_column(default="open", server_default="open")
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('utc', now())")
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=text("TIMEZONE('utc', now())")
    )
    assigned_to: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.user_id"))

    user: Mapped["User"] = relationship(back_populates="tickets")
