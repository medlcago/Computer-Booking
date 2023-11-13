from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline_main import computer_management_menu

router = Router()


@router.callback_query(F.data == "computer_management")
async def computer_management(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text="Панель управления компьютерами", reply_markup=computer_management_menu())
