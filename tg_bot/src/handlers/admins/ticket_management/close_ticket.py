from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from keyboards.callbackdata import Ticket
from keyboards.inline_utils import create_inline_keyboard
from states.admins import CloseTicket
from utils.api_methods import TicketAPI

router = Router()


@router.callback_query(Ticket.filter())
async def close_ticket(call: CallbackQuery, callback_data: Ticket, state: FSMContext):
    ticket_id = callback_data.ticket_id
    assigned_to = callback_data.assigned_to

    await call.answer()
    sent_message = await call.message.reply("Введите ваш ответ ниже:")
    await state.set_state(CloseTicket.text)
    await state.update_data(
        ticket_id=ticket_id,
        assigned_to=assigned_to,
        sent_message_id=sent_message.message_id
    )


@router.message(CloseTicket.text)
async def close_ticket(message: Message, bot: Bot, state: FSMContext, ticket_api: TicketAPI):
    data = await state.get_data()

    ticket_id = data.get("ticket_id")
    assigned_to = data.get("assigned_to")
    sent_message_id = data.get("sent_message_id")
    text = message.text

    if ticket := await ticket_api.close_ticket(ticket_id=ticket_id):
        await bot.delete_message(chat_id=message.chat.id, message_id=sent_message_id)
        await message.reply(
            text=f"✅ Вы успешно ответили на тикет.\n"
                 f"<b>ID:</b> {ticket_id}\n"
                 f"<b>Заголовок:</b> {ticket.get('title')}\n"
                 f"<b>Получатель:</b> {assigned_to}",
            reply_markup=create_inline_keyboard(width=1, close="❌ Закрыть")
        )
        await bot.send_message(
            chat_id=assigned_to,
            text=f"Вам пришел ответ на ваш тикет.\n"
                 f"<b>ID:</b> {ticket_id}\n"
                 f"<b>Заголовок:</b> {ticket.get('title')}\n\n"
                 f"{text}")

    await state.clear()
