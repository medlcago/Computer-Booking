from datetime import datetime

from pydantic import BaseModel, Field


class CreateBooking(BaseModel):
    user_id: int
    computer_id: int
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: datetime = Field(default_factory=datetime.utcnow)


class GetBooking(CreateBooking):
    class Config:
        from_attributes = True
