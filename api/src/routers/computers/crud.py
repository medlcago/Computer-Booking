from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, DBAPIError
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


async def get_computers_by_category(db: AsyncSession, category: Categories, limit: int = None) -> Sequence[Computer]:
    if limit:
        stmt = select(Computer).options(selectinload(Computer.bookings)).filter_by(category=category).limit(limit=limit)
    else:
        stmt = select(Computer).options(selectinload(Computer.bookings)).filter_by(category=category)

    result = await db.execute(stmt)
    computers = result.scalars().all()
    if computers:
        return computers
    raise HTTPException(status_code=404, detail=f"Computers with {category} category not found.")


async def get_all_computers(db: AsyncSession, limit: int = None) -> Sequence[Computer]:
    if limit:
        stmt = select(Computer).options(selectinload(Computer.bookings)).limit(limit=limit).order_by(
            Computer.ram, Computer.id)
    else:
        stmt = select(Computer).options(selectinload(Computer.bookings)).order_by(
            Computer.ram, Computer.id)

    result = await db.execute(stmt)
    computers = result.scalars().all()
    if computers:
        return computers
    raise HTTPException(status_code=404, detail="Computers not found.")


async def update_computer_component(db: AsyncSession, data: dict, computer_id: int) -> Computer:
    computer = await db.scalar(select(Computer).filter_by(computer_id=computer_id))
    if computer is None:
        raise HTTPException(status_code=404, detail=f"Computer with ID {computer_id} not found.")

    try:
        value = int(data["component_value"])
    except (ValueError, TypeError):
        value = str(data["component_value"])

    try:
        await db.execute(update(Computer).filter_by(computer_id=computer_id).values(**{data["component_name"]: value}))
        await db.commit()
        return computer
    except DBAPIError:
        raise HTTPException(status_code=400, detail="Incorrect data has been transmitted. Please, try again.")


async def update_computer(db: AsyncSession, data: dict, computer_id: int) -> Computer:
    computer = await db.scalar(select(Computer).filter_by(computer_id=computer_id))
    if computer is None:
        raise HTTPException(status_code=404, detail=f"Computer with ID {computer_id} not found.")

    try:
        await db.execute(update(Computer).filter_by(computer_id=computer_id).values(**data))
        await db.commit()
        return computer
    except IntegrityError:
        raise HTTPException(status_code=409, detail=f"Computer with ID {computer_id} already exists.")


async def delete_computer(db: AsyncSession, computer_id: int) -> dict:
    computer = await db.scalar(select(Computer).filter_by(computer_id=computer_id))
    if computer is None:
        raise HTTPException(status_code=404, detail=f"Computer with ID {computer_id} not found.")

    await db.delete(computer)
    await db.commit()
    return {
        "status": f"The computer with ID {computer_id} was successfully deleted."
    }
