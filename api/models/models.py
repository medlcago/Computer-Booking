from datetime import datetime

from sqlalchemy import BIGINT, ForeignKey, TIMESTAMP, MetaData, String, CheckConstraint, text, func
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(BIGINT, unique=True)
    fullname: Mapped[str] = mapped_column(String(length=255))
    username: Mapped[str | None] = mapped_column(String(length=255))
    email_address: Mapped[str | None] = mapped_column(String(length=255))
    password: Mapped[str] = mapped_column(String(length=255))
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_blocked: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    balance: Mapped[int] = mapped_column(CheckConstraint("balance >= 0"), default=0)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=text(f"({func.now()} AT TIME ZONE 'UTC')"))

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=text(f"({func.now()} AT TIME ZONE 'UTC')"),
        onupdate=text(f"({func.now()} AT TIME ZONE 'UTC')")
    )

    bookings: Mapped[list["Booking"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan")


class Computer(Base):
    __tablename__ = 'computers'

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


class Booking(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(User.user_id))
    computer_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(Computer.computer_id))
    start_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    end_time: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))

    user: Mapped["User"] = relationship(back_populates="bookings")
    computer: Mapped["Computer"] = relationship(back_populates="bookings")
