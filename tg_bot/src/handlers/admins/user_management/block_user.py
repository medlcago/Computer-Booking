from aiogram import Router, F
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
    await call.message.answer("Вы хотите заблокировать пользователя.\nПожалуйста, введите его ID")
    await state.set_state(BlockUser.user_id)


@router.message(BlockUser.user_id)
async def block_user(message: Message, state: FSMContext, user_api: UserAPI):
    await state.clear()
    try:
        user_id = int(message.text)
    except ValueError:
        await message.reply(f"<i>ID</i> должен быть целым числом!")
        return

    is_blocked = await user_api.update_user_details(user_id=user_id, is_blocked=True)
    if is_blocked:
        await message.reply(f"Пользователь <code>{user_id}</code> был заблокирован!")
    else:
        await message.reply(f"Не удалось заблокировать пользователя <code>{user_id}</code>!")
