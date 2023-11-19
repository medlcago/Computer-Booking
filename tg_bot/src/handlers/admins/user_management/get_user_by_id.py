from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from filters import IsAdmin
from keyboards.inline_utils import create_inline_keyboard
from states.admins import UserInfo
from utils.api_methods import UserAPI
from utils.misc import generate_info_about_user_message

router = Router()


@router.callback_query(F.data == "get_user_by_id", IsAdmin())
async def get_user_by_id(call: CallbackQuery, state: FSMContext):
    """
    Информация о пользователе (1)
    """
    await call.answer(cache_time=15)
    sent_message = await call.message.answer(
        text="Вы хотите получить информацию о пользователе.\nПожалуйста, введите его ID"
    )
    await state.set_state(UserInfo.user_id)
    await state.update_data(sent_message_id=sent_message.message_id)


@router.message(UserInfo.user_id, F.text.regexp(r"^(\d+)$"))
async def get_user_by_id(message: Message, bot: Bot, state: FSMContext, user_api: UserAPI):
    """
    Информация о пользователе (2)
    """
    data = await state.get_data()
    sent_message_id = data.get("sent_message_id")
    user_id = int(message.text)
    user = await user_api.get_user_by_id(user_id=user_id)
    if user:
        message_text = generate_info_about_user_message(user=user)
        await message.reply(
            text=message_text,
            reply_markup=create_inline_keyboard(width=1, close="❌ Закрыть")
        )
    else:
        await message.reply(text=f"Не удалось получить информацию по ID <code>{user_id}</code>")

    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message_id)
    await state.clear()
