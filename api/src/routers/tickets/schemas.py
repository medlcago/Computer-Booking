from datetime import datetime

from pydantic import BaseModel

from api.enums import TicketStatus


class CreateTicket(BaseModel):
    title: str
    assigned_to: int


class TicketResponse(CreateTicket):
    status: TicketStatus
    created_at: datetime
    updated_at: datetime
    id: int
