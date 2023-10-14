from enum import Enum

from pydantic import BaseModel, Field


class Categories(str, Enum):
    vip = "VIP"
    regular = "Regular"


class BaseComputer(BaseModel):
    computer_id: int
    brand: str
    model: str
    cpu: str
    ram: int
    storage: int
    gpu: str
    description: str | None = Field(default=None, max_length=256)
    category: Categories

    class Config:
        from_attributes = True


class Components(str, Enum):
    brand = "brand"
    model = "model"
    cpu = "cpu"
    ram = "ram"
    storage = "storage"
    gpu = "gpu"
    description = "description"
    category = "category"
