from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from filters import IsAdmin
from states.admins import DeleteUser
from utils.api_methods import UserAPI

router = Router()


@router.callback_query(F.data == "delete_user", IsAdmin())
async def delete_user(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=15)
    sent_message = await call.message.answer(
        text="Вы хотите удалить пользователя из БД.\n"
             "Пожалуйста, введите его ID"
    )
    await state.set_state(DeleteUser.user_id)
    await state.update_data(sent_message_id=sent_message.message_id)


@router.message(DeleteUser.user_id, F.text.regexp(r"^(\d+)$"))
async def delete_user(message: Message, state: FSMContext, user_api: UserAPI):
    data = await state.get_data()
    sent_message_id = data.get("sent_message_id")
    user_id = int(message.text)

    if await user_api.delete_user(user_id=user_id):
        await message.reply(f"Пользователь <code>{user_id}</code> был успешно удален!")
    else:
        await message.reply(f"Не удалось удалить пользователя <code>{user_id}</code>!")

    await message.bot.delete_message(chat_id=message.chat.id, message_id=sent_message_id)
    await state.clear()
