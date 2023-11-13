from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "close")
async def close_handler(call: CallbackQuery) -> None:
    await call.answer()
    await call.message.delete()
