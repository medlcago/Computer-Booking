from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline_main import ticket_management_menu

router = Router()


@router.callback_query(F.data == "ticket_management")
async def ticket_management(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(text="Панель управления тикетами", reply_markup=ticket_management_menu())
