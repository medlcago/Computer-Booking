from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline_main import user_management_menu

router = Router()


@router.callback_query(F.data == "user_management")
async def user_management(call: CallbackQuery):
    await call.answer(cache_time=15)
    await call.message.edit_text(text="Панель управления пользователями", reply_markup=user_management_menu())
