from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from filters import IsAdmin
from keyboards.inline_utils import create_inline_keyboard
from states.admins import ChangeBalance
from utils.api_methods import UserAPI

router = Router()


@router.callback_query(F.data == "change_balance", IsAdmin())
async def change_balance(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=15)
    await call.message.answer("Вы хотите начислить баланс пользователю.\nПожалуйста, введите его ID и сумму начисления\n<b>5272546957:500</b>")
    await state.set_state(ChangeBalance.user_id)


@router.message(ChangeBalance.user_id)
async def change_balance(message: Message, state: FSMContext, user_api: UserAPI):
    await state.clear()
    try:
        user_id, amount = map(int, message.text.split(":"))
    except ValueError:
        await message.reply(f"<i>Данные</i> должны быть целыми числами!")
        return

    user = await user_api.get_user_by_id(user_id=user_id)
    keyboard = create_inline_keyboard(width=1, close="❌ Закрыть")

    if user:
        current_balance = user.get("balance")
        if data := await user_api.update_user_details(
                user_id=user_id,
                balance=current_balance + amount
        ):
            new_balance = data.get("balance")
            await message.reply(
                text=f"На баланс пользователя <code>{user_id}</code> было добавлено <b>{amount} RUB.</b>\nТекущий баланс: <b>{new_balance} RUB.</b>",
                reply_markup=keyboard
            )
        else:
            await message.reply(
                text=f"Не удалось начислить </b>{amount} RUB</b> пользователю <code>{user_id}</code>",
                reply_markup=keyboard
            )
    else:
        await message.reply(
            text=f"Не удалось получить информацию по ID <code>{user_id}</code>",
            reply_markup=keyboard
        )
