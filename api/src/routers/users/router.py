from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Body, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.user import User
from database import get_db
from routers.users.schemas import CreateUser, BaseUser, ChangePasswordData, ChangePasswordResponse
from services.auth import auth_guard_key
from services.auth import auth_service

router = APIRouter(prefix="/users", tags=["User Operation"], dependencies=[Depends(auth_guard_key)])


@router.post("/", response_model=BaseUser, summary="Регистрация нового пользователя", status_code=status.HTTP_201_CREATED)
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
        user.password = auth_service.hash_password(password=user.password)
        db.add(user)
        await db.commit()
        return user
    except IntegrityError:
        raise HTTPException(status_code=409, detail=f"User with ID {user.user_id} already exists.")


@router.get("/", response_model=list[BaseUser], summary="Получение информации о всех пользователях")
async def get_all_users(limit: Annotated[int | None, Query(gt=0)] = None, db: AsyncSession = Depends(get_db)):
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


@router.patch("/id{user_id}", response_model=ChangePasswordResponse, summary="Сменить пароль пользователя")
async def change_user_password(user_id: int, data: ChangePasswordData, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).filter_by(user_id=user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    if auth_service.verify_password(data.password, user.password):
        if data.password == data.new_password:
            raise HTTPException(status_code=400, detail="The new password must not match the old password.")
        user.password = auth_service.hash_password(data.new_password)
        await db.commit()

        response_data = ChangePasswordResponse(
            user_id=user_id,
            new_password=data.new_password
        )

        return response_data
    raise HTTPException(status_code=401, detail="Invalid user password.")
