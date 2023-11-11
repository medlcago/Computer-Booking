from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from routers.payments.schemas import CreatePayment, PaymentResponse
from services.auth import auth_guard_key
from . import crud

router = APIRouter(prefix="/payments", tags=["Payments"], dependencies=[Depends(auth_guard_key)])


@router.post("/", response_model=PaymentResponse, summary="Создание нового платежа",
             status_code=status.HTTP_201_CREATED)
async def create_payment(data: CreatePayment, db: AsyncSession = Depends(get_db)):
    return await crud.create_payment(db=db, data=data.model_dump(exclude_unset=True))


@router.get("/user/id{user_id}", response_model=list[PaymentResponse], summary="История платежей пользователя")
async def get_user_payments(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_user_payments(db=db, user_id=user_id)
