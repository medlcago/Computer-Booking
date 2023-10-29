from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud

from database import get_db
from routers.booking.schemas import CreateBooking, GetBooking
from services.auth import auth_guard_key

router = APIRouter(prefix="/bookings", tags=["Booking Operation"], dependencies=[Depends(auth_guard_key)])


@router.post("/", response_model=CreateBooking, summary="Создать новый заказ", status_code=status.HTTP_201_CREATED)
async def create_booking(data: CreateBooking, db: AsyncSession = Depends(get_db)):
    return await crud.create_booking(db=db, data=data.model_dump())


@router.get("/", response_model=list[GetBooking], summary="Получить список всех заказов")
async def get_all_bookings(limit: int = None, db: AsyncSession = Depends(get_db)):
    return await crud.get_all_bookings(db=db, limit=limit)


@router.get("/user/id{user_id}", response_model=list[GetBooking], summary="Получить список заказов пользователя")
async def get_bookings_by_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_bookings_by_user_id(db=db, user_id=user_id)


@router.delete("/id{booking_id}", summary="Удалить заказ")
async def delete_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_booking(db=db, booking_id=booking_id)
