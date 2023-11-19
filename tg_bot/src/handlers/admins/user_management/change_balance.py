from aiogram import Router, F, Bot
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
    sent_message = await call.message.answer(
        text="Вы хотите начислить баланс пользователю.\n"
             "Пожалуйста, введите его ID и сумму начисления\n"
             "<b>5272546957:500</b>"
    )
    await state.set_state(ChangeBalance.user_id)
    await state.update_data(sent_message_id=sent_message.message_id)


@router.message(ChangeBalance.user_id, F.text.regexp(r"^(\d+):(-?\d+)$"))
async def change_balance(message: Message, bot: Bot, state: FSMContext, user_api: UserAPI):
    data = await state.get_data()
    sent_message_id = data.get("sent_message_id")
    user_id, amount = map(int, message.text.split(":"))
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
                text=f"На баланс пользователя <code>{user_id}</code> было добавлено <b>{amount} RUB.</b>\n"
                     f"Текущий баланс: <b>{new_balance} RUB.</b>",
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

    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message_id)
    await state.clear()
