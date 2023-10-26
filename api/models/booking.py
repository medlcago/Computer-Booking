from sqlalchemy import Column, MetaData, BIGINT, ForeignKey, TIMESTAMP

from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

from api.models.computer import Computer
from api.models.user import User

metadata = MetaData()

Base = declarative_base(metadata=metadata)

class Booking(Base):
    __tablename__ = 'bookings'

    id: int = Column(BIGINT, primary_key=True, index=True)
    user_id: int = Column(BIGINT, ForeignKey(User.user_id))
    computer_id: int = Column(BIGINT, ForeignKey(Computer.computer_id))
    start_time: datetime = Column(TIMESTAMP, nullable=False)
    end_time: datetime = Column(TIMESTAMP, nullable=False)

    user = relationship("User", back_populates="booking")
    computer = relationship("Computer", back_populates="booking")

