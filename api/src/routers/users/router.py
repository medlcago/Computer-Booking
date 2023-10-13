import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.user import User
from database import get_db
from depends import auth_guard_key
from routers.users.schemas import CreateUser, BaseUser, ChangePassword
from routers.users.utils import hash_password, verify_password

router = APIRouter(prefix="/user/operations", tags=["User Operation"], dependencies=[Depends(auth_guard_key)])


@router.post("/create-user", response_model=BaseUser)
async def create_user(data: CreateUser, db: AsyncSession = Depends(get_db)):
    try:
        user = User(**data.model_dump())
        user.password = hash_password(password=user.password)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except Exception as e:
        logging.error(f"User creation error: {e}")
        raise HTTPException(status_code=500, detail="User creation error")


@router.get("/get-user/", response_model=BaseUser)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).filter_by(user_id=user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@router.get("/get-all-users", response_model=list[BaseUser])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    users = (await db.scalars(select(User))).all()
    if users:
        return users
    raise HTTPException(status_code=404, detail="Users do not exist.")


@router.patch("/change-password", response_model=ChangePassword, response_model_exclude={"password"})
async def change_user_password(data: ChangePassword, db: AsyncSession = Depends(get_db)):
    user = await db.scalar(select(User).filter_by(user_id=data.user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    if verify_password(data.password, user.password):
        user.password = hash_password(data.new_password)
        await db.commit()
        return data
    raise HTTPException(status_code=401, detail="Invalid user password.")
