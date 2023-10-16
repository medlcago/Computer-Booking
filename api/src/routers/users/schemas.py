from enum import Enum

from pydantic import BaseModel, Field


class BaseUser(BaseModel):
    user_id: int
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class CreateUser(BaseUser):
    password: str


class ChangePassword(BaseModel):
    password: str = Field(min_length=8, max_length=30, description="Текущий пароль")
    new_password: str = Field(min_length=8, max_length=30, description="Новый пароль")

    class Config:
        from_attributes = True
