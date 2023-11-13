from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline_main import payment_management_menu

router = Router()


@router.callback_query(F.data == "payment_management")
async def payment_management(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text="Панель управления платежами", reply_markup=payment_management_menu())
