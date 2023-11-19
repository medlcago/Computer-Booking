from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from states.admins import AddComputer
from utils.api_methods import ComputerAPI

router = Router()


@router.callback_query(F.data == "add_computer")
async def add_computer(call: CallbackQuery, state: FSMContext):
    await call.answer()
    sent_message = await call.message.answer(
        "Вы хотите добавить компьютер.\nПожалуйста, введите данные в следующем формате:\n"
        "<b>brand:</b> Бренд [*]\n"
        "<b>model:</b> Модель [*]\n"
        "<b>cpu:</b> Процессор [*]\n"
        "<b>ram:</b> ОЗУ [*]\n"
        "<b>storage:</b> Объем диска [*]\n"
        "<b>gpu:</b> Видеокарта [*]\n"
        "<b>description:</b> Описание (Макс. 255 символов)\n"
        "<b>category:</b> Категория (VIP или Regular) [*]\n"
        "<b>price_per_hour:</b> Цена за час [*]\n\n"
        "<i>* - Параметр является обязательным</i>")
    await state.set_state(AddComputer.computer_data)
    await state.update_data(sent_message_id=sent_message.message_id)


@router.message(AddComputer.computer_data, F.text)
async def add_computer(message: Message, bot: Bot, state: FSMContext, computer_api: ComputerAPI):
    data = await state.get_data()
    sent_message_id = data.get("sent_message_id")
    data = message.text.split('\n')
    computer_data = {}
    for line in data:
        key, value = line.split(':')
        computer_data[key.strip()] = value.strip()
    if computer := await computer_api.add_new_computer(**computer_data):
        await message.reply(f"Компьютер успешно добавлен.\nID компьютера: <b>{computer.get('computer_id')}</b>")
    else:
        await message.reply(
            text="Не удалось добавить компьютер в базу данных.\n"
                 "Пожалуйста, проверьте правильность введенных данных!"
        )

    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message_id)
    await state.clear()
