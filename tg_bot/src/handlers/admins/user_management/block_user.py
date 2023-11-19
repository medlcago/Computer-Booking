from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from filters import IsAdmin
from states.admins import BlockUser
from utils.api_methods import UserAPI

router = Router()


@router.callback_query(F.data == "block_user", IsAdmin())
async def block_user(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=15)
    sent_message = await call.message.answer("Вы хотите заблокировать пользователя.\nПожалуйста, введите его ID")
    await state.set_state(BlockUser.user_id)
    await state.update_data(sent_message_id=sent_message.message_id)


@router.message(BlockUser.user_id, F.text.regexp(r"^(\d+)$"))
async def block_user(message: Message, bot: Bot, state: FSMContext, user_api: UserAPI):
    data = await state.get_data()
    sent_message_id = data.get("sent_message_id")
    user_id = int(message.text)

    is_blocked = await user_api.update_user_details(user_id=user_id, is_blocked=True)
    if is_blocked:
        await message.reply(f"Пользователь <code>{user_id}</code> был заблокирован!")
    else:
        await message.reply(f"Не удалось заблокировать пользователя <code>{user_id}</code>!")

    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message_id)
    await state.clear()
