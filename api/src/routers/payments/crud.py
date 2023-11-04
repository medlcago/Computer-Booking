from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import Payment


async def create_payment(db: AsyncSession, data: dict):
    try:
        payment = Payment(**data)
        db.add(payment)
        await db.commit()
        return payment
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Data integrity error when creating a payment.")


async def get_user_payments(db: AsyncSession, user_id: int):
    stmt = select(Payment).filter_by(user_id=user_id)
    result = await db.execute(stmt)
    payments = result.scalars().all()
    if payments is None:
        raise HTTPException(status_code=404, detail=f"Payments of the user with id {user_id} were not found.")
    return payments
