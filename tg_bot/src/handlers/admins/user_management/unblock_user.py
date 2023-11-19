from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from filters import IsAdmin
from states.admins import UnBlockUser
from utils.api_methods import UserAPI

router = Router()


@router.callback_query(F.data == "unblock_user", IsAdmin())
async def unblock_user(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=15)
    sent_message = await call.message.answer("Вы хотите разблокировать пользователя.\nПожалуйста, введите его ID")
    await state.set_state(UnBlockUser.user_id)
    await state.update_data(sent_message_id=sent_message.message_id)


@router.message(UnBlockUser.user_id, F.text.regexp(r"^(\d+)$"))
async def unblock_user(message: Message, bot: Bot, state: FSMContext, user_api: UserAPI):
    data = await state.get_data()
    sent_message_id = data.get("sent_message_id")
    user_id = int(message.text)

    is_blocked = await user_api.update_user_details(user_id=user_id, is_blocked=False)
    if is_blocked:
        await message.reply(f"Пользователь <code>{user_id}</code> был разблокирован!")
    else:
        await message.reply(f"Не удалось разблокировать пользователя <code>{user_id}</code>!")

    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message_id)
    await state.clear()
