from datetime import datetime

from pydantic import BaseModel, Field


class CreatePayment(BaseModel):
    user_id: int
    amount: int
    payload: str | None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class PaymentResponse(CreatePayment):
    id: int
