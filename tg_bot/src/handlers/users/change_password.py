from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from states.users import ChangePassword
from utils.api_methods import UserAPI

router = Router()


@router.callback_query(F.data == "change_password")
async def change_password(call: CallbackQuery, state: FSMContext):
    await call.answer()
    sent_message_bot_1 = await call.message.answer(
        "Вы хотите сменить пароль.\nПожалуйста, введите свой текущий пароль ниже:")
    await state.set_state(ChangePassword.current_password)
    await state.update_data(sent_message_bot_1_id=sent_message_bot_1.message_id)


@router.message(ChangePassword.current_password, F.text)
async def change_password(message: Message, state: FSMContext):
    await state.update_data(current_password=message.text)
    sent_message_bot_2 = await message.answer("Введите новый пароль ниже:")
    await state.set_state(ChangePassword.new_password)
    await state.update_data(sent_message_user_1_id=message.message_id)
    await state.update_data(sent_message_bot_2_id=sent_message_bot_2.message_id)


@router.message(ChangePassword.new_password, F.text)
async def change_password(message: Message, state: FSMContext, user_api: UserAPI):
    data = await state.get_data()
    sent_message_bot_1_id = data.get("sent_message_bot_1_id")
    sent_message_bot_2_id = data.get("sent_message_bot_2_id")
    sent_message_user_1_id = data.get("sent_message_user_1_id")
    user_id = message.from_user.id
    current_password = data.get("current_password")
    new_password = message.text

    if await user_api.change_user_password(
            user_id=user_id,
            current_password=current_password,
            new_password=new_password
    ):
        await message.answer(f"Вы успешно сменили пароль.\nНовый пароль: <tg-spoiler>{new_password}</tg-spoiler>")
    else:
        await message.answer("Не удалось сменить пароль.\nПожалуйста, повторите попытку.")

    await message.bot.delete_message(chat_id=message.chat.id, message_id=sent_message_bot_1_id)
    await message.bot.delete_message(chat_id=message.chat.id, message_id=sent_message_bot_2_id)
    await message.bot.delete_message(chat_id=message.chat.id, message_id=sent_message_user_1_id)
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await state.clear()
