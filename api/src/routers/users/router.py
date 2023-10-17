import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.user import User
from database import get_db
from depends import auth_guard_key
from routers.users.schemas import CreateUser, BaseUser, ChangePassword
from routers.users.utils import hash_password, verify_password

router = APIRouter(prefix="/users", tags=["User Operation"], dependencies=[Depends(auth_guard_key)])
logger = logging.getLogger(__name__)


@router.post("/", response_model=BaseUser, summary="Регистрация нового пользователя")
async def create_user(
        data: Annotated[CreateUser, Body(examples=[{
            "user_id": 1000,
            "first_name": "Alexander",
            "last_name": "Korolev",
            "password": "28DxTiPdux"
        }])],
        db: AsyncSession = Depends(get_db)):
    try:
        user = User(**data.model_dump())
        user.password = hash_password(password=user.password)
        db.add(user)
        await db.commit()
        return user
    except Exception as e:
        logger.error(f"User creation error: {e}")
        raise HTTPException(status_code=500, detail="User creation error")


@router.get("/", response_model=list[BaseUser], summary="Получение информации о всех пользователях")
async def get_all_users(limit: int = None, db: AsyncSession = Depends(get_db)):
    if limit:
        users = (await db.scalars(select(User).limit(limit=limit))).all()
    else:
        users = (await db.scalars(select(User))).all()
    if users:
        return users
    raise HTTPException(status_code=404, detail="Users do not exist.")


@router.get("/id{user_id}", response_model=BaseUser,
            summary="Получение информации о пользователи по его идентификатору")
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).filter_by(user_id=user_id))
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    return user


@router.patch("/id{user_id}", response_model=ChangePassword, response_model_exclude={"password"},
              summary="Сменить пароль пользователя")
async def change_user_password(user_id: int, data: ChangePassword, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).filter_by(user_id=user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    if verify_password(data.password, user.password):
        if data.password == data.new_password:
            raise HTTPException(status_code=400, detail="The new password must not match the old password.")
        user.password = hash_password(data.new_password)
        await db.commit()
        return data
    raise HTTPException(status_code=401, detail="Invalid user password.")
