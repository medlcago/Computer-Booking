from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from api.models import Computer


async def update_reserved_status(db: AsyncSession, computer_id: int = None, category: str = None):
    current_time = datetime.now(timezone.utc)
    async with db.begin():
        stmt = select(Computer).options(selectinload(Computer.bookings))
        if computer_id:
            stmt = stmt.filter_by(computer_id=computer_id)

        if category:
            stmt = stmt.filter_by(category=category)

        computers = await db.execute(stmt)
        for computer in computers.scalars().all():
            if computer.bookings:
                is_reserved = False
                for booking in computer.bookings:
                    if booking.start_time <= current_time < booking.end_time:
                        is_reserved = True
                        break
                computer.is_reserved = is_reserved
