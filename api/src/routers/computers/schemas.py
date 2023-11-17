from pydantic import BaseModel, Field

from api.enums import ComputerCategories


class BaseComputer(BaseModel):
    brand: str
    model: str
    cpu: str
    ram: int
    storage: int
    gpu: str
    description: str | None = Field(default=None, max_length=255)
    category: ComputerCategories
    price_per_hour: int

    class Config:
        from_attributes = True


class ComputerResponse(BaseComputer):
    computer_id: int
    is_reserved: bool = Field(default=False)


class UpdateComputerComponent(BaseModel):
    brand: str | None = Field(default=None)
    model: str | None = Field(default=None)
    cpu: str | None = Field(default=None)
    ram: int | None = Field(default=None)
    storage: int | None = Field(default=None)
    gpu: str | None = Field(default=None)
    description: str | None = Field(default=None, max_length=256)
    category: ComputerCategories | None = Field(default=None)


class UpdatedComputerComponent(UpdateComputerComponent):
    pass
