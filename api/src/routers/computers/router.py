from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy import select, update, delete
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.computer import Computer
from database import get_db
from routers.computers.schemas import BaseComputer, Categories, UpdateComputerComponent
from services.auth import auth_guard_key

router = APIRouter(prefix="/computers", tags=["Computer Operation"], dependencies=[Depends(auth_guard_key)])


@router.post("/", summary="Добавить новый компьютер")
async def add_new_computer(data: Annotated[BaseComputer, Body(examples=[{
    "computer_id": 1000,
    "brand": "IRU",
    "model": "310H5GMA",
    "cpu": "Intel Core i5 11400F",
    "ram": 16,
    "storage": 1024,
    "gpu": "NVIDIA GeForce RTX 3060",
    "description": "Gaming powerhouse with high refresh rate display and powerful GPU.",
    "category": "VIP"
}])], db: AsyncSession = Depends(get_db)):
    try:
        computer = Computer(**data.model_dump(exclude_none=True))
        db.add(computer)
        await db.commit()
        return {
            "status": "Computer added successfully.",
            "ID": computer.computer_id
        }
    except IntegrityError:
        raise HTTPException(status_code=409, detail=f"Computer with ID {computer.computer_id} already exists.")


@router.get("/id{computer_id}", response_model=BaseComputer,
            summary="Получение информации о компьютере по его идентификатору")
async def get_computer_by_id(computer_id: int, db: AsyncSession = Depends(get_db)):
    computer = await db.scalar(select(Computer).filter_by(computer_id=computer_id))
    if computer is None:
        raise HTTPException(status_code=404, detail=f"Computer with ID {computer_id} not found.")
    return computer


@router.get("/{category}", response_model=list[BaseComputer],
            summary="Получение информации о компьютерах конкретной категории")
async def get_computers_by_category(category: Categories, limit: int = None, db: AsyncSession = Depends(get_db)):
    if limit:
        computers = (await db.scalars(select(Computer).filter_by(category=category).limit(limit=limit))).all()
    else:
        computers = (await db.scalars(select(Computer).filter_by(category=category))).all()
    return computers


@router.get("/", response_model=list[BaseComputer], summary="Получение информации о всех компьютерах")
async def get_all_computers(limit: int = None, db: AsyncSession = Depends(get_db)):
    if limit:
        computers = (await db.scalars(select(Computer).limit(limit=limit).order_by(Computer.ram))).all()
    else:
        computers = (await db.scalars(select(Computer).order_by(Computer.ram))).all()
    return computers


@router.patch("/id{computer_id}", response_model=BaseComputer,
              summary="Сменить информацию о компоненте компьютера по его идентификатору")
async def update_computer_component(computer_id: int,
                                    data: Annotated[UpdateComputerComponent, Body(examples=[
                                        {
                                            "component_name": "cpu",
                                            "component_value": "AMD Ryzen 5 5600x"
                                        }
                                    ])],
                                    db: AsyncSession = Depends(get_db)):
    computer = await db.scalar(select(Computer).filter_by(computer_id=computer_id))
    if computer is None:
        raise HTTPException(status_code=404, detail=f"Computer with ID {computer_id} not found.")

    try:
        value = int(data.component_value)
    except (ValueError, TypeError):
        value = str(data.component_value)

    try:
        await db.execute(update(Computer).filter_by(computer_id=computer_id).values(**{data.component_name: value}))
        await db.commit()
        return computer
    except DBAPIError:
        raise HTTPException(status_code=400, detail="Incorrect data has been transmitted. Please, try again.")


@router.put("/id{computer_id}", response_model=BaseComputer,
            summary="Сменить всю информацию о компьютере по его идентификатору")
async def update_computer(computer_id: int, data: Annotated[BaseComputer, Body(examples=[{
    "computer_id": 1000,
    "brand": "IRU",
    "model": "310H5GMA",
    "cpu": "Intel Core i5 11400F",
    "ram": 16,
    "storage": 1024,
    "gpu": "NVIDIA GeForce RTX 3060",
    "description": None,
    "category": "VIP"
}])], db: AsyncSession = Depends(get_db)):
    computer = await db.scalar(select(Computer).filter_by(computer_id=computer_id))
    if computer is None:
        raise HTTPException(status_code=404, detail=f"Computer with ID {computer_id} not found.")

    try:
        await db.execute(update(Computer).filter_by(computer_id=computer_id).values(**data.model_dump(exclude_none=True)))
        await db.commit()
        return computer
    except IntegrityError:
        raise HTTPException(status_code=409, detail=f"Computer with ID {computer_id} already exists.")


@router.delete("/id{computer_id}", summary="Удалить компьютер по его идентификатору")
async def delete_computer(computer_id: int, db: AsyncSession = Depends(get_db)):
    computer = await db.scalar(select(Computer).filter_by(computer_id=computer_id))
    if computer is None:
        raise HTTPException(status_code=404, detail=f"Computer with ID {computer_id} not found.")

    await db.execute(delete(Computer).filter_by(computer_id=computer_id))
    await db.commit()
    return {
        "status": f"The computer with ID {computer_id} was successfully deleted."
    }
