from aiogram import Router, F, flags
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "close")
@flags.skip
async def close_handler(call: CallbackQuery) -> None:
    await call.answer()
    await call.message.delete()
