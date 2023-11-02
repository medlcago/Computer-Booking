from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api.models import Computer
from routers.computers.schemas import Categories


async def add_new_computer(db: AsyncSession, data: dict) -> Computer:
    try:
        computer = Computer(**data)
        db.add(computer)
        await db.commit()
        return computer
    except IntegrityError:
        raise HTTPException(status_code=409, detail=f"Computer with ID {computer.computer_id} already exists.")


async def get_computer_by_id(db: AsyncSession, computer_id: int) -> Computer:
    stmt = select(Computer).options(selectinload(Computer.bookings))
    result = await db.execute(stmt)
    computer = result.scalar()

    if computer is None:
        raise HTTPException(status_code=404, detail=f"Computer with ID {computer_id} not found.")
    return computer


async def get_computers_by_category(db: AsyncSession, category: Categories, limit: int = None, is_reserved: bool = None) -> Sequence[Computer]:
    if limit:
        stmt = select(Computer).options(selectinload(Computer.bookings)).filter_by(category=category).limit(limit=limit)
    else:
        stmt = select(Computer).options(selectinload(Computer.bookings)).filter_by(category=category)

    if is_reserved is not None:
        stmt = stmt.filter_by(is_reserved=is_reserved)

    result = await db.execute(stmt)
    computers = result.scalars().all()
    return computers


async def get_all_computers(db: AsyncSession, limit: int = None, is_reserved: bool = None) -> Sequence[Computer]:
    if limit:
        stmt = select(Computer).options(selectinload(Computer.bookings)).limit(limit=limit).order_by(
            Computer.ram, Computer.id)
    else:
        stmt = select(Computer).options(selectinload(Computer.bookings)).order_by(
            Computer.ram, Computer.computer_id)

    if is_reserved is not None:
        stmt = stmt.filter_by(is_reserved=is_reserved)

    result = await db.execute(stmt)
    computers = result.scalars().all()
    return computers


async def update_computer_components(db: AsyncSession, data: dict, computer_id: int) -> dict:
    if data:
        stmt = update(Computer).filter_by(computer_id=computer_id).values(**data)
        result = await db.execute(stmt)

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Computer with ID {computer_id} not found.")
        await db.commit()
    return data


async def delete_computer(db: AsyncSession, computer_id: int) -> dict:
    computer = await db.scalar(select(Computer).filter_by(computer_id=computer_id))
    if computer is None:
        raise HTTPException(status_code=404, detail=f"Computer with ID {computer_id} not found.")

    await db.delete(computer)
    await db.commit()
    return {
        "status": f"The computer with ID {computer_id} was successfully deleted."
    }
