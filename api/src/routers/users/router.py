import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models.user import User
from database import get_async_session
from routers.users.schemas import CreateUser, BaseUser

router = APIRouter(prefix="/user/operations", tags=["User Operation"])


@router.post("/create-user", response_model=BaseUser)
async def create_user(data: CreateUser, db: AsyncSession = Depends(get_async_session)):
    try:
        user = User(**data.model_dump())
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except Exception as e:
        logging.error(f"User creation error: {e}")
        raise HTTPException(status_code=500, detail="User creation error")


@router.get("/get-user", response_model=BaseUser)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_async_session)):
    user = await db.scalar(select(User).filter_by(user_id=user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
