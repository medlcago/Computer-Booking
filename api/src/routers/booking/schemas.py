from datetime import datetime

from pydantic import BaseModel, Field


class BaseBooking(BaseModel):
    user_id: int
    computer_id: int
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class BookingResponse(BaseBooking):
    id: int
