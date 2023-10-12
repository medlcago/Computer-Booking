from pydantic import BaseModel


class BaseUser(BaseModel):
    user_id: int
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class CreateUser(BaseUser):
    password: str
