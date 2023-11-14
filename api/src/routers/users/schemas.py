from datetime import datetime

from pydantic import BaseModel, Field

from routers.booking.schemas import BookingResponse
from routers.payments.schemas import PaymentResponse


class BaseUser(BaseModel):
    user_id: int
    fullname: str
    username: str | None = Field(default=None)
    phone_number: str

    class Config:
        from_attributes = True


class UserResponse(BaseUser):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    phone_number: str = Field(default=None)
    is_admin: bool | None = Field(default=None)
    is_blocked: bool | None = Field(default=None)
    is_active: bool | None = Field(default=None)
    balance: int | None = Field(default=None)


class FullUserResponse(UserResponse):
    bookings: list["BookingResponse"]
    payments: list["PaymentResponse"]


class CreateUser(BaseUser):
    password: str = Field(
        min_length=8,
        max_length=30,
        description="Пароль пользователя")


class UpdateUserDetails(BaseModel):
    phone_number: str | None = Field(default=None)
    is_admin: bool | None = Field(default=None)
    is_blocked: bool | None = Field(default=None)
    is_active: bool | None = Field(default=None)
    balance: int | None = Field(default=None)


class UpdatedUserDetails(UpdateUserDetails):
    pass


class ChangeUserPassword(BaseModel):
    current_password: str = Field(min_length=8, max_length=30, description="Текущий пароль")
    new_password: str = Field(min_length=8, max_length=30, description="Новый пароль")

    class Config:
        from_attributes = True


class ChangedUserPassword(BaseModel):
    user_id: int = Field(description="ID пользователя")
    new_password: str = Field(description="Новый пароль")

    class Config:
        from_attributes = True
