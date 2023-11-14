from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from filters import IsAdmin
from keyboards.inline_utils import create_inline_keyboard
from states.admins import UserInfo
from utils.api_methods import UserAPI
from utils.misc import generate_info_about_user_message

router = Router()


@router.callback_query(F.data == "info_about_user", IsAdmin())
async def info_about_user(call: CallbackQuery, state: FSMContext):
    """
    Информация о пользователе (1)
    """
    await call.answer(cache_time=60)
    await call.message.answer("Вы хотите получить информацию о пользователе.\nПожалуйста, введите его ID")
    await state.set_state(UserInfo.user_id)


@router.message(UserInfo.user_id)
async def info_about_user(message: Message, state: FSMContext, user_api: UserAPI):
    """
    Информация о пользователе (2)
    """
    await state.clear()
    try:
        user_id = int(message.text)
    except ValueError:
        await message.reply(f"<i>ID</i> должен быть целым числом!")
        return

    user = await user_api.get_user_by_id(user_id=user_id)
    if user:
        message_text = generate_info_about_user_message(user=user)
        await message.reply(
            text=message_text,
            reply_markup=create_inline_keyboard(width=1, close="❌ Закрыть")
        )
    else:
        await message.reply(text=f"Не удалось получить информацию по ID <code>{user_id}</code>")
