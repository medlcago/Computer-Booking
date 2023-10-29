from datetime import datetime

from pydantic import BaseModel, Field, field_validator, EmailStr


class BaseUser(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    username: str | None = Field(default=None)
    email_address: EmailStr | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class CreateUser(BaseUser):
    password: str = Field(
        min_length=8,
        max_length=30,
        description="Пароль пользователя")

    @field_validator("password")
    def password_complexity(cls, password):
        if not any(char.isupper() for char in password):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not any(char.isdigit() for char in password):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        return password


class ChangePasswordData(BaseModel):
    password: str = Field(min_length=8, max_length=30, description="Текущий пароль")
    new_password: str = Field(min_length=8, max_length=30, description="Новый пароль")

    @field_validator("new_password")
    def password_complexity(cls, new_password):
        if not any(char.isupper() for char in new_password):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not any(char.isdigit() for char in new_password):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        return new_password

    class Config:
        from_attributes = True


class ChangePasswordResponse(BaseModel):
    user_id: int = Field(description="ID пользователя")
    new_password: str = Field(description="Новый пароль")

    class Config:
        from_attributes = True
