from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline_utils import create_inline_keyboard
from templates.texts import BOT_INFORMATION
from utils.api_methods import UserAPI

router = Router()


@router.callback_query(F.data == "bot_information")
async def bot_information(call: CallbackQuery, user_api: UserAPI):
    number_users = len(await user_api.get_all_users())
    await call.answer()
    await call.message.edit_text(
        text=BOT_INFORMATION.format(number_users=number_users),
        reply_markup=create_inline_keyboard(
            width=1,
            show_menu="Вернуться в меню"
        ),
        disable_web_page_preview=True
    )
