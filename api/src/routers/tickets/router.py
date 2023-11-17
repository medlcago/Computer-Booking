from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.enums import TicketStatus
from database import get_db
from routers.tickets.schemas import CreateTicket, TicketResponse
from services.auth import auth_guard_key
from . import crud

router = APIRouter(prefix="/tickets", tags=["Tickets"], dependencies=[Depends(auth_guard_key)])


@router.post("/", response_model=TicketResponse, summary="Создание нового тикета", status_code=status.HTTP_201_CREATED)
async def create_ticket(data: CreateTicket, db: AsyncSession = Depends(get_db)):
    return await crud.create_ticket(db=db, data=data.model_dump())


@router.patch("/id{ticket_id}", response_model=TicketResponse, summary="Закрытие тикета")
async def close_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.close_ticket(db=db, ticket_id=ticket_id)


@router.get("/", response_model=list[TicketResponse], summary="Получить все тикеты")
async def get_all_tickets(ticket_status: TicketStatus | None = None, db: AsyncSession = Depends(get_db)):
    return await crud.get_all_tickets(db=db, status=ticket_status)


@router.get("/user/id{user_id}", response_model=list[TicketResponse], summary="Получить тикеты пользователя")
async def get_user_tickets_by_user_id(user_id: int, ticket_status: TicketStatus | None = None, db: AsyncSession = Depends(get_db)):
    return await crud.get_tickets_by_user_id(db=db, user_id=user_id, status=ticket_status)
