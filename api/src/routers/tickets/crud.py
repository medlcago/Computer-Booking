from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.enums import TicketStatus
from api.models import Ticket


async def create_ticket(db: AsyncSession, data: dict) -> Ticket:
    try:
        ticket = Ticket(**data)
        db.add(ticket)
        await db.commit()
        return ticket
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Data integrity error when creating a ticket.")


async def close_ticket(db: AsyncSession, ticket_id: int) -> Ticket:
    ticket = await db.scalar(select(Ticket).filter_by(id=ticket_id))
    if ticket is None:
        raise HTTPException(status_code=404, detail=f"Ticket with ID {ticket_id} not found.")
    ticket.status = "closed"
    await db.commit()
    await db.refresh(ticket)
    return ticket


async def get_all_tickets(db: AsyncSession, status: TicketStatus | None = None) -> Sequence[Ticket]:
    stmt = select(Ticket).order_by(Ticket.id)
    if status is not None:
        stmt = stmt.filter_by(status=status)
    result = await db.execute(stmt)
    tickets = result.scalars().all()
    return tickets


async def get_tickets_by_user_id(db: AsyncSession, user_id: int, status: TicketStatus | None = None) -> Sequence[Ticket]:
    stmt = select(Ticket).filter_by(assigned_to=user_id).order_by(Ticket.id)
    if status is not None:
        stmt = stmt.filter_by(status=status)
    result = await db.execute(stmt)
    tickets = result.scalars().all()
    return tickets


async def get_ticket_by_id(db: AsyncSession, ticket_id: int) -> Ticket:
    ticket = await db.scalar(select(Ticket).filter_by(id=ticket_id))
    if ticket is None:
        raise HTTPException(status_code=404, detail=f"Ticket with ID {ticket_id} not found.")
    return ticket
