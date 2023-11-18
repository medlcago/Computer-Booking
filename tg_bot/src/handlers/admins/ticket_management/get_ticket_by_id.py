from aiogram import Router, F
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
    await call.message.answer("Вы хотите получить информацию о тикете.\nПожалуйста, введите его ID")
    await state.set_state(TicketInfo.ticket_id)


@router.message(TicketInfo.ticket_id)
async def get_ticket_by_id(message: Message, state: FSMContext, ticket_api: TicketAPI):
    await state.clear()
    try:
        ticket_id = int(message.text)
    except ValueError:
        await message.reply(f"<i>ID</i> должен быть целым числом!")
        return

    ticket = await ticket_api.get_ticket_by_id(ticket_id=ticket_id)
    if ticket:
        message_text, keyboard = generate_ticket_message(ticket, 1, 1)
        await message.reply(
            text=message_text,
            reply_markup=keyboard
        )
    else:
        await message.reply(text=f"Не удалось получить информацию по тикету с ID <code>{ticket_id}</code>")
