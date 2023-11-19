from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from states.admins import TicketInfo
from utils.api_methods import TicketAPI
from utils.misc import generate_ticket_message

router = Router()


@router.callback_query(F.data == "get_ticket_by_id")
async def get_ticket_by_id(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=15)
    sent_message = await call.message.answer(
        text="Вы хотите получить информацию о тикете.\n"
             "Пожалуйста, введите его ID"
    )
    await state.set_state(TicketInfo.ticket_id)
    await state.update_data(sent_message_id=sent_message.message_id)


@router.message(TicketInfo.ticket_id, F.text.regexp(r"^(\d+)$"))
async def get_ticket_by_id(message: Message, bot: Bot, state: FSMContext, ticket_api: TicketAPI):
    data = await state.get_data()
    sent_message_id = data.get("sent_message_id")
    ticket_id = int(message.text)
    ticket = await ticket_api.get_ticket_by_id(ticket_id=ticket_id)

    if ticket:
        message_text, keyboard = generate_ticket_message(ticket, 1, 1)
        await message.reply(
            text=message_text,
            reply_markup=keyboard
        )
    else:
        await message.reply(text=f"Не удалось получить информацию по тикету с ID <code>{ticket_id}</code>")

    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message_id)
    await state.clear()
