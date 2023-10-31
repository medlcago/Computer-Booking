from typing import Annotated

from fastapi import APIRouter, Depends, Body, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from routers.users.schemas import (
    CreateUser,
    ChangeUserPassword,
    ChangedUserPassword,
    UserResponse,
    UpdateUserDetails,
    UpdatedUserDetails)
from services.auth import auth_guard_key
from . import crud

router = APIRouter(prefix="/users", tags=["User Operation"], dependencies=[Depends(auth_guard_key)])


@router.post("/", response_model=UserResponse, summary="Регистрация нового пользователя",
             status_code=status.HTTP_201_CREATED)
async def create_user(
        data: Annotated[CreateUser, Body(examples=[{
            "user_id": 1000,
            "first_name": "Alexander",
            "last_name": "Korolev",
            "username": "medlcago",
            "email_address": "medlcago@example.com",
            "password": "28DxTiPdux"
        }])],
        db: AsyncSession = Depends(get_db)):
    return await crud.create_user(db=db, data=data.model_dump())


@router.patch("/id{user_id}/", response_model=UpdatedUserDetails, response_model_exclude_unset=True,
              summary="Обновление данных пользователя")
async def update_user_details(user_id: int, data: UpdateUserDetails, db: AsyncSession = Depends(get_db)):
    return await crud.update_user_details(db=db, user_id=user_id, data=data.model_dump(exclude_unset=True))


@router.get("/", response_model=list[UserResponse], summary="Получение информации о всех пользователях")
async def get_all_users(limit: Annotated[int | None, Query(gt=0)] = None, db: AsyncSession = Depends(get_db)):
    return await crud.get_all_users(db=db, limit=limit)


@router.get("/id{user_id}", response_model=UserResponse,
            summary="Получение информации о пользователи по его идентификатору")
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_user_by_id(db=db, user_id=user_id)


@router.patch("/id{user_id}/password", response_model=ChangedUserPassword, summary="Сменить пароль пользователя")
async def change_user_password(user_id: int, data: ChangeUserPassword, db: AsyncSession = Depends(get_db)):
    return await crud.change_user_password(db=db, data=data.model_dump(), user_id=user_id)


@router.delete("/id{user_id}", summary="Удалить пользователя по его идентификатору")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_user(db=db, user_id=user_id)
