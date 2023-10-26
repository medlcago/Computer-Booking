from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import User
from routers.users.schemas import ChangePasswordResponse
from services.auth import auth_service


async def create_user(db: AsyncSession, data: dict) -> User:
    try:
        user = User(**data)
        user.password = auth_service.hash_password(password=user.password)
        db.add(user)
        await db.commit()
        return user
    except IntegrityError:
        raise HTTPException(status_code=409, detail=f"User with ID {user.user_id} already exists.")


async def get_all_users(db: AsyncSession, limit: int = None) -> Sequence[User]:
    if limit:
        users = (await db.scalars(select(User).limit(limit=limit))).all()
    else:
        users = (await db.scalars(select(User))).all()
    if users:
        return users
    raise HTTPException(status_code=404, detail="Users do not exist.")


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    user = await db.scalar(select(User).filter_by(user_id=user_id))
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    return user


async def change_user_password(db: AsyncSession, data: dict, user_id: int):
    user = await db.scalar(select(User).filter_by(user_id=user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    if auth_service.verify_password(data["password"], user.password):
        if data["password"] == data["new_password"]:
            raise HTTPException(status_code=400, detail="The new password must not match the old password.")
        user.password = auth_service.hash_password(data["new_password"])
        await db.commit()

        response_data = ChangePasswordResponse(
            user_id=user_id,
            new_password=data["new_password"]
        )

        return response_data
    raise HTTPException(status_code=401, detail="Invalid user password.")
