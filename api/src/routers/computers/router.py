from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.computer import Computer
from database import get_db
from depends import auth_guard_key
from routers.computers.schemas import BaseComputer, Categories

router = APIRouter(prefix="/computer/operations", tags=["Computer Operation"])


@router.post("/add-computer")
async def add_new_computer(data: BaseComputer, db: AsyncSession = Depends(get_db)):
    computer = Computer(**data.model_dump())
    db.add(computer)
    await db.commit()
    await db.refresh(computer)
    return {
        "status": "Computer added successfully."
    }


@router.get("/get-computers", response_model=list[BaseComputer])
async def get_computers_by_category(category: Categories, db: AsyncSession = Depends(get_db)):
    computers = (await db.scalars(select(Computer).filter_by(category=category))).all()
    return computers


@router.get("/get-all-computers", response_model=list[BaseComputer])
async def get_all_computers(db: AsyncSession = Depends(get_db)):
    computers = (await db.scalars(select(Computer).order_by(Computer.ram))).all()
    return computers


if __name__ == '__main__':
    coms = [
        Computer(brand="Apple", model="MacBook Pro", cpu="Intel Core i7", ram=16, storage=512,
                 gpu="AMD Radeon Pro 5300M", description="Powerful and sleek laptop for professionals."),
        Computer(brand="Dell", model="XPS 15", cpu="Intel Core i9", ram=32, storage=1_000,
                 gpu="NVIDIA GeForce RTX 3070",
                 description="High-performance laptop with stunning display and graphics."),
        Computer(brand="HP", model="Pavilion", cpu="AMD Ryzen 5", ram=8, storage=256, gpu="AMD Radeon Graphics",
                 description="Affordable and reliable laptop for everyday use."),
        Computer(brand="Lenovo", model="ThinkPad X1 Carbon", cpu="Intel Core i5", ram=16, storage=512,
                 gpu="Intel UHD Graphics", description="Durable and lightweight laptop for business professionals."),
        Computer(brand="Asus", model="ROG Strix G17", cpu="AMD Ryzen 9", ram=32, storage=1_000,
                 gpu="NVIDIA GeForce RTX 3080",
                 description="Gaming powerhouse with high refresh rate display and powerful GPU."),
        Computer(brand="Acer", model="Predator Helios 300", cpu="Intel Core i7", ram=16, storage=1_000,
                 gpu="NVIDIA GeForce GTX 1660 Ti", description="Gaming laptop with excellent performance and cooling."),
        Computer(brand="Microsoft", model="Surface Laptop 4", cpu="AMD Ryzen 7", ram=16, storage=512,
                 gpu="AMD Radeon Graphics", description="Sleek and portable laptop with great battery life.")
    ]
