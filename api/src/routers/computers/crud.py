from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.enums import ComputerCategories
from api.models import Computer
from routers.computers.utils import update_reserved_status


async def add_new_computer(db: AsyncSession, data: dict) -> Computer:
    try:
        computer = Computer(**data)
        db.add(computer)
        await db.commit()
        return computer
    except IntegrityError:
        raise HTTPException(status_code=409, detail=f"Computer with ID {computer.computer_id} already exists.")


async def get_computer_by_id(db: AsyncSession, computer_id: int) -> Computer:
    await update_reserved_status(db=db, computer_id=computer_id)

    stmt = select(Computer).filter_by(computer_id=computer_id)
    result = await db.execute(stmt)
    computer = result.scalar()

    if computer is None:
        raise HTTPException(status_code=404, detail=f"Computer with ID {computer_id} not found.")
    return computer


async def get_computers_by_category(db: AsyncSession, category: ComputerCategories, is_reserved: bool | None = None) -> Sequence[Computer]:
    await update_reserved_status(db=db, category=category)

    stmt = select(Computer).filter_by(category=category).order_by(Computer.computer_id)
    if is_reserved is not None:
        stmt = stmt.filter_by(is_reserved=is_reserved)

    result = await db.execute(stmt)
    computers = result.scalars().all()
    return computers


async def get_all_computers(db: AsyncSession, is_reserved: bool | None = None) -> Sequence[Computer]:
    await update_reserved_status(db=db)

    stmt = select(Computer).order_by(Computer.computer_id)
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
