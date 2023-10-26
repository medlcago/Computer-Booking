from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError, DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import Computer
from routers.computers.schemas import Categories


async def add_new_computer(db: AsyncSession, data: dict) -> dict:
    try:
        computer = Computer(**data)
        db.add(computer)
        await db.commit()
        return {
            "status": "Computer added successfully.",
            "ID": computer.computer_id
        }
    except IntegrityError:
        raise HTTPException(status_code=409, detail=f"Computer with ID {computer.computer_id} already exists.")


async def get_computer_by_id(db: AsyncSession, computer_id: int) -> Computer:
    computer = await db.scalar(select(Computer).filter_by(computer_id=computer_id))
    if computer is None:
        raise HTTPException(status_code=404, detail=f"Computer with ID {computer_id} not found.")
    return computer


async def get_computers_by_category(db: AsyncSession, category: Categories, limit: int = None) -> Sequence[Computer]:
    if limit:
        computers = (await db.scalars(select(Computer).filter_by(category=category).limit(limit=limit))).all()
    else:
        computers = (await db.scalars(select(Computer).filter_by(category=category))).all()
    return computers


async def get_all_computers(db: AsyncSession, limit: int = None) -> Sequence[Computer]:
    if limit:
        computers = (await db.scalars(select(Computer).limit(limit=limit).order_by(Computer.ram))).all()
    else:
        computers = (await db.scalars(select(Computer).order_by(Computer.ram))).all()
    return computers


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

    await db.execute(delete(Computer).filter_by(computer_id=computer_id))
    await db.commit()
    return {
        "status": f"The computer with ID {computer_id} was successfully deleted."
    }
