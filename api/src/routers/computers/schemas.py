from enum import Enum

from pydantic import BaseModel, Field


class Categories(str, Enum):
    vip = "VIP"
    regular = "Обычный"


class BaseComputer(BaseModel):
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
