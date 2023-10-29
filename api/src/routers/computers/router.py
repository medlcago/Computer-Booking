from typing import Annotated

from fastapi import APIRouter, Depends, Body, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from routers.computers.schemas import BaseComputer, Categories, UpdateComputerComponent
from services.auth import auth_guard_key
from . import crud

router = APIRouter(prefix="/computers", tags=["Computer Operation"], dependencies=[Depends(auth_guard_key)])


@router.post("/", response_model=BaseComputer, summary="Добавить новый компьютер", status_code=status.HTTP_201_CREATED)
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
    return await crud.add_new_computer(db=db, data=data.model_dump(exclude_none=True))


@router.get("/id{computer_id}", response_model=BaseComputer,
            summary="Получение информации о компьютере по его идентификатору")
async def get_computer_by_id(computer_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_computer_by_id(db=db, computer_id=computer_id)


@router.get("/{category}", response_model=list[BaseComputer],
            summary="Получение информации о компьютерах конкретной категории")
async def get_computers_by_category(category: Categories, limit: int = None, db: AsyncSession = Depends(get_db)):
    return await crud.get_computers_by_category(db=db, category=category, limit=limit)


@router.get("/", response_model=list[BaseComputer], summary="Получение информации о всех компьютерах")
async def get_all_computers(limit: int = None, db: AsyncSession = Depends(get_db)):
    return await crud.get_all_computers(db=db, limit=limit)


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
    return await crud.update_computer_component(db=db, data=data.model_dump(), computer_id=computer_id)


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
    return await crud.update_computer(db=db, data=data.model_dump(), computer_id=computer_id)


@router.delete("/id{computer_id}", summary="Удалить компьютер по его идентификатору")
async def delete_computer(computer_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_computer(db=db, computer_id=computer_id)
