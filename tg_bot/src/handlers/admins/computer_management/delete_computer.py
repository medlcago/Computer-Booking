from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from states.admins import DeleteComputer
from utils.api_methods import ComputerAPI

router = Router()


@router.callback_query(F.data == "delete_computer")
async def delete_computer(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=15)
    sent_message = await call.message.answer(
        text="Вы хотите удалить компьютер.\n"
             "Пожалуйста, введите его ID"
    )
    await state.set_state(DeleteComputer.computer_id)
    await state.update_data(sent_message_id=sent_message.message_id)


@router.message(DeleteComputer.computer_id, F.text.regexp(r"^(\d+)$"))
async def delete_computer(message: Message, bot: Bot, state: FSMContext, computer_api: ComputerAPI):
    data = await state.get_data()
    sent_message_id = data.get("sent_message_id")
    computer_id = int(message.text)

    if await computer_api.delete_computer(computer_id=int(computer_id)):
        await message.reply("Компьютер был успешно удален!")
    else:
        await message.reply("Не удалось удалить компьютер!")

    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message_id)
    await state.clear()
