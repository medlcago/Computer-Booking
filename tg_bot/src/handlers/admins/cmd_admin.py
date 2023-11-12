from aiogram import Router, F
from aiogram.filters.command import Command
from aiogram.types import CallbackQuery
from aiogram.types import Message

from filters import IsAdmin
from keyboards.inline_main import admin_menu

router = Router()


@router.message(Command(commands="admin"), IsAdmin())
async def command_admin(message: Message):
    await message.reply(
        text="Панель администратора\nПожалуйста, выберите нужно действие.",
        reply_markup=admin_menu()
    )


@router.callback_query(F.data == "show_admin_menu")
async def show_admin_menu(call: CallbackQuery):
    await call.answer(cache_time=30)
    await call.message.edit_text(
        text="Панель администратора\nПожалуйста, выберите нужно действие.",
        reply_markup=admin_menu()
    )


@router.message(Command(commands="admin"))
async def command_admin(message: Message):
    await message.reply("Nice try, bro! 🤣")
