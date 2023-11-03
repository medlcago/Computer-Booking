from aiogram import types, Router, flags, F, html
from aiogram.filters.command import CommandStart
from aiogram.types import ReplyKeyboardRemove

from keyboards.inline_main import main_menu_button
from templates.texts import COMMAND_START

router = Router()


@router.message(F.content_type == "contact")
@flags.user_contact
async def get_user_contact(message: types.Message, user_password: str):
    await message.answer(
        f"✅ Номер телефона успешно подтвержден.\n\n"
        f"<b>Ваш пароль:</b> <tg-spoiler>{user_password}</tg-spoiler>\n\n"
        f"<i>❗️Он может пригодиться для подтверждения действий, не потеряйте его)</i>",
        reply_markup=ReplyKeyboardRemove())
    await message.answer(
        text=COMMAND_START.format(fullname=html.quote(message.from_user.full_name)),
        reply_markup=main_menu_button
    )


@router.message(CommandStart())
async def command_start(message: types.Message):
    await message.answer(
        text=COMMAND_START.format(fullname=html.quote(message.from_user.full_name)),
        reply_markup=main_menu_button
    )
