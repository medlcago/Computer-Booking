from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline_utils import create_inline_keyboard
from templates.texts import MY_PROFILE
from utils.api_methods import UserAPI

router = Router()


@router.callback_query(F.data == "my_profile")
async def show_my_profile(call: CallbackQuery, user_api: UserAPI):
    user = await user_api.get_user_by_id(user_id=call.from_user.id)
    await call.answer()

    user_id = call.from_user.id
    balance = user.get("balance")
    phone_number = user.get("phone_number")

    await call.message.edit_text(
        text=MY_PROFILE.format(user_id=user_id, balance=balance, phone_number=phone_number),
        reply_markup=create_inline_keyboard(
            width=1,
            show_menu="Вернуться в меню",
            change_password="Сменить пароль")
    )
