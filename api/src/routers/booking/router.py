from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from routers.booking.schemas import (
    BaseBooking,
    BookingResponse)
from . import crud

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=BookingResponse, summary="Создать новый заказ", status_code=status.HTTP_201_CREATED)
async def create_computer_booking(
        data: Annotated[BaseBooking, Body(examples=[{
            "user_id": 1000,
            "computer_id": 15,
            "start_time": datetime.utcnow(),
            "end_time": datetime.utcnow()
        }])],
        db: AsyncSession = Depends(get_db)):
    return await crud.create_computer_booking(db=db, data=data.model_dump())


@router.get("/", response_model=list[BookingResponse], summary="Получить список всех заказов")
async def get_all_computer_bookings(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_computer_bookings(db=db)


@router.get("/user/id{user_id}", response_model=list[BookingResponse], summary="Получить список заказов пользователя")
async def get_computer_bookings_by_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_computer_bookings_by_user_id(db=db, user_id=user_id)


@router.delete("/id{booking_id}", summary="Удалить заказ")
async def delete_computer_booking(booking_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_computer_booking(db=db, booking_id=booking_id)
