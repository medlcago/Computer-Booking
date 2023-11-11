from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import Booking
from api.models import Computer


async def create_computer_booking(db: AsyncSession, data: dict) -> Booking:
    try:
        computer_id = data.get("computer_id")
        computer = await db.get(Computer, computer_id)

        if computer is None:
            raise HTTPException(status_code=404, detail=f"Computer with ID {computer_id} not found.")

        if computer.is_reserved:
            raise HTTPException(status_code=400, detail=f"Computer with ID {computer_id} is already reserved.")

        computer.is_reserved = True
        booking = Booking(**data, computer=computer)
        db.add(booking)
        await db.commit()
        return booking
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Data integrity error when creating a booking.")


async def get_all_computer_bookings(db: AsyncSession) -> Sequence[Booking]:
    stmt = select(Booking).order_by(Booking.id)
    result = await db.execute(stmt)
    bookings = result.scalars().all()
    return bookings


async def get_computer_bookings_by_user_id(db: AsyncSession, user_id: int) -> Sequence[Booking]:
    stmt = select(Booking).filter_by(user_id=user_id).order_by(Booking.id)
    result = await db.execute(stmt)
    bookings = result.scalars().all()
    return bookings


async def delete_computer_booking(db: AsyncSession, booking_id: int) -> dict:
    booking = await db.scalar(select(Booking).filter_by(id=booking_id))
    if booking is None:
        raise HTTPException(status_code=404, detail=f"Booking with ID {booking_id} not found.")

    await db.delete(booking)
    await db.commit()
    return {
        "status": f"The booking with ID {booking_id} was successfully deleted."
    }
