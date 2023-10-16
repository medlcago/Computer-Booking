from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.computer import Computer
from database import get_db
from routers.computers.schemas import BaseComputer, Categories, Components

router = APIRouter(prefix="/computers", tags=["Computer Operation"])


@router.post("/")
async def add_new_computer(data: BaseComputer, db: AsyncSession = Depends(get_db)):
    computer = Computer(**data.model_dump())
    db.add(computer)
    await db.commit()
    return {
        "status": "Computer added successfully.",
        "ID": computer.computer_id
    }


@router.get("/id{computer_id}", response_model=BaseComputer)
async def get_computer_by_id(computer_id: int, db: AsyncSession = Depends(get_db)):
    computer = await db.scalar(select(Computer).filter_by(computer_id=computer_id))
    if computer is None:
        raise HTTPException(status_code=404, detail=f"Computer with ID {computer_id} not found.")
    return computer


@router.get("/{category}", response_model=list[BaseComputer])
async def get_computers_by_category(category: Categories, db: AsyncSession = Depends(get_db)):
    computers = (await db.scalars(select(Computer).filter_by(category=category))).all()
    return computers


@router.get("/", response_model=list[BaseComputer])
async def get_all_computers(db: AsyncSession = Depends(get_db)):
    computers = (await db.scalars(select(Computer).order_by(Computer.ram))).all()
    return computers


@router.patch("/id{computer_id}", response_model=BaseComputer)
async def update_computer_component(computer_id: Annotated[int, Path(..., description="Уникальный ID компьютера")],
                                    component: Annotated[Components, Query(..., description="Компонент компьютера")],
                                    value: Annotated[str | int, Query(..., description="Значение компонента")],
                                    db: AsyncSession = Depends(get_db)):
    computer = await db.scalar(select(Computer).filter_by(computer_id=computer_id))

    if computer is None:
        raise HTTPException(status_code=404, detail=f"Computer with ID {computer_id} not found.")

    try:
        value = int(value)
    except (ValueError, TypeError):
        value = str(value)

    await db.execute(update(Computer).filter_by(computer_id=computer_id).values(**{component: value}))
    await db.commit()
    return computer


@router.put("/id{computer_id}", response_model=BaseComputer)
async def update_computer(computer_id: int, data: BaseComputer, db: AsyncSession = Depends(get_db)):
    computer = await db.scalar(select(Computer).filter_by(computer_id=computer_id))
    if computer is None:
        raise HTTPException(status_code=404, detail=f"Computer with ID {computer_id} not found.")

    await db.execute(update(Computer).filter_by(computer_id=computer_id).values(**data.model_dump()))
    await db.commit()
    return computer


@router.delete("/id{computer_id}")
async def delete_computer(computer_id: int, db: AsyncSession = Depends(get_db)):
    computer = await db.scalar(select(Computer).filter_by(computer_id=computer_id))
    if computer is None:
        raise HTTPException(status_code=404, detail=f"Computer with ID {computer_id} not found.")

    await db.execute(delete(Computer).filter_by(computer_id=computer_id))
    await db.commit()
    return {
        "status": f"The computer with ID {computer_id} was successfully deleted."
    }