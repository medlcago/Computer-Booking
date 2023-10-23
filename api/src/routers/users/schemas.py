from datetime import datetime

from pydantic import BaseModel, Field


class BaseUser(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    created_at: datetime = None

    class Config:
        from_attributes = True


class CreateUser(BaseUser):
    password: str = Field(min_length=8, max_length=30, description="Пароль пользователя")


class ChangePasswordData(BaseModel):
    password: str = Field(min_length=8, max_length=30, description="Текущий пароль")
    new_password: str = Field(min_length=8, max_length=30, description="Новый пароль")

    class Config:
        from_attributes = True


class ChangePasswordResponse(BaseModel):
    status: bool = Field(default=True, description="Статус операции")
    user_id: int = Field(description="ID пользователя")
    new_password: str = Field(min_length=8, max_length=30, description="Новый пароль")

    class Config:
        from_attributes = True
