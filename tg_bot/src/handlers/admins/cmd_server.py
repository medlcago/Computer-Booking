from aiogram import types, Router, F
from aiogram.filters.command import Command

from filters import IsAdmin
from utils.misc import get_server_system_info
from keyboards.inline_utils import create_inline_keyboard

router = Router()


@router.message(Command(commands="server"), IsAdmin())
async def command_server(message: types.Message):
    result = get_server_system_info()
    await message.reply(result)


@router.callback_query(F.data == "server_info", IsAdmin())
async def command_server(call: types.CallbackQuery):
    result = get_server_system_info()
    await call.message.edit_text(
        text=result,
        reply_markup=create_inline_keyboard(
            width=1,
            show_admin_menu="🔙 Вернуться в админ панель",
            close="❌ Закрыть"
        ))
    await call.answer()
