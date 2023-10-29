from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.models import Booking


async def create_booking(db: AsyncSession, data: dict) -> Booking:
    try:
        booking = Booking(**data)
        db.add(booking)
        await db.commit()
        return booking
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Data integrity error when creating a booking.")


async def get_all_bookings(db: AsyncSession, limit: int = None) -> Sequence[Booking]:
    if limit:
        stmt = select(Booking).options(selectinload(Booking.user), selectinload(Booking.computer)).limit(limit=limit)
    else:
        stmt = select(Booking).options(selectinload(Booking.user), selectinload(Booking.computer))
    result = await db.execute(stmt)
    bookings = result.scalars().all()
    if bookings:
        return bookings
    raise HTTPException(status_code=404, detail="Bookings not found.")


async def get_bookings_by_user_id(db: AsyncSession, user_id: int) -> Sequence[Booking]:
    stmt = select(Booking).options(selectinload(Booking.user), selectinload(Booking.computer)).filter_by(user_id=user_id)
    result = await db.execute(stmt)
    bookings = result.scalars().all()
    if bookings:
        return bookings
    raise HTTPException(status_code=404, detail="Bookings not found.")


async def delete_booking(db: AsyncSession, booking_id: int) -> dict:
    booking = await db.scalar(select(Booking).filter_by(id=booking_id))
    if booking is None:
        raise HTTPException(status_code=404, detail=f"Booking with ID {booking_id} not found.")

    await db.delete(booking)
    await db.commit()
    return {
        "status": f"The booking with ID {booking_id} was successfully deleted."
    }
