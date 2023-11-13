from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline_main import booking_management_menu

router = Router()


@router.callback_query(F.data == "booking_management")
async def booking_management(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text="Панель управления бронированиями", reply_markup=booking_management_menu())
