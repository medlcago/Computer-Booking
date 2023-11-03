from aiogram import types, Router, flags, F
from aiogram.filters.command import CommandStart
from aiogram.types import ReplyKeyboardRemove

from keyboards.inline_main import main_menu

router = Router()


@router.message(F.content_type == "contact")
@flags.user_contact
async def get_user_contact(message: types.Message, user_password: str):
    await message.answer(
        f"✅ Ваш номер телефона успешно подтвержден.\n\n"
        f"<b>Ваш пароль:</b> <tg-spoiler>{user_password}</tg-spoiler>\n\n"
        f"<i>❗️Он может пригодиться для подтверждения действий, не потеряйте его)</i>",
        reply_markup=ReplyKeyboardRemove())


@router.message(CommandStart())
async def command_start(message: types.Message):
    await message.answer("Меню", reply_markup=main_menu())
