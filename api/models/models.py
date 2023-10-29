from datetime import datetime

from sqlalchemy import Column, BIGINT, ForeignKey, TIMESTAMP, MetaData, String, INTEGER, BOOLEAN
from sqlalchemy.orm import relationship, declarative_base, Mapped

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = 'users'

    id: int = Column(BIGINT, primary_key=True, index=True)
    user_id: int = Column(BIGINT, nullable=False, unique=True)
    first_name: str = Column(String(length=255), nullable=False)
    last_name: str = Column(String(length=255), nullable=False)
    password: str = Column(String(length=255), nullable=False)
    created_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)
    updated_at: datetime = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow,
                                  onupdate=datetime.utcnow)

    booking: Mapped["Booking"] = relationship("Booking", back_populates="user")


class Computer(Base):
    __tablename__ = 'computers'

    id: int = Column(BIGINT, primary_key=True, index=True)
    computer_id: int = Column(BIGINT, nullable=False, unique=True)
    brand: str = Column(String(length=255), nullable=False)
    model: str = Column(String(length=255), nullable=False)
    cpu: str = Column(String(length=255), nullable=False)
    ram: int = Column(INTEGER, nullable=False)
    storage: int = Column(INTEGER, nullable=False)
    gpu: str = Column(String(length=255), nullable=False)
    description: str = Column(String(length=255), default=None)
    category: str = Column(String(length=255), nullable=False)
    is_reserved: bool = Column(BOOLEAN, nullable=False, default=False)

    booking: Mapped["Booking"] = relationship("Booking", back_populates="computer")


class Booking(Base):
    __tablename__ = 'bookings'

    id: int = Column(BIGINT, primary_key=True, index=True)
    user_id: int = Column(BIGINT, ForeignKey(User.user_id))
    computer_id: int = Column(BIGINT, ForeignKey(Computer.computer_id))
    start_time: datetime = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time: datetime = Column(TIMESTAMP(timezone=True), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="booking")
    computer: Mapped["Computer"] = relationship("Computer", back_populates="booking")
