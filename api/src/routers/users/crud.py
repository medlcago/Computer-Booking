from typing import Sequence

from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import User
from routers.users.schemas import ChangedUserPassword
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


async def update_user_details(db: AsyncSession, user_id: int, data: dict) -> User:
    if data:
        try:
            stmt = update(User).filter_by(user_id=user_id).values(**data)
            result = await db.execute(stmt)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Data integrity error")

        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
        await db.commit()
        data = await db.scalar(select(User).filter_by(user_id=user_id))
    return data


async def get_all_users(
        db: AsyncSession,
        is_admin: bool | None = None,
        is_blocked: bool | None = None,
        is_active: bool | None = None) -> Sequence[User]:
    stmt = select(User)
    if is_admin is not None:
        stmt = stmt.filter_by(is_admin=is_admin)

    if is_blocked is not None:
        stmt = stmt.filter_by(is_blocked=is_blocked)

    if is_active is not None:
        stmt = stmt.filter_by(is_active=is_active)

    result = await db.execute(stmt)
    users = result.scalars().all()
    return users


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    stmt = select(User).filter_by(user_id=user_id)
    result = await db.execute(stmt)
    user = result.scalar()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    return user


async def change_user_password(db: AsyncSession, data: dict, user_id: int) -> ChangedUserPassword:
    user = await db.scalar(select(User).filter_by(user_id=user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    if auth_service.verify_password(data["current_password"], user.password):
        if data["current_password"] == data["new_password"]:
            raise HTTPException(status_code=400, detail="The new password must not match the old password.")
        user.password = auth_service.hash_password(data["new_password"])
        await db.commit()

        response_data = ChangedUserPassword(
            user_id=user_id,
            new_password=data["new_password"]
        )

        return response_data
    raise HTTPException(status_code=401, detail="Invalid user password.")


async def delete_user(db: AsyncSession, user_id: int) -> dict:
    user = await db.scalar(select(User).filter_by(user_id=user_id))
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")

    await db.delete(user)
    await db.commit()
    return {
        "status": f"User with ID {user_id} was successfully deleted."
    }


async def get_user_by_id_with_full_information(db: AsyncSession, user_id) -> User:
    user = await db.scalar(select(User).filter_by(user_id=user_id).options(selectinload(User.bookings)).options(selectinload(User.payments)))
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    return user
