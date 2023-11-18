import json

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.storage.redis import Redis
from aiogram.types import CallbackQuery

from keyboards.callbackdata import PageNumber
from keyboards.inline_utils import create_inline_keyboard
from utils.api_methods import TicketAPI
from utils.misc import generate_ticket_message

router = Router()


@router.callback_query(F.data == "open_tickets")
async def open_tickets(call: CallbackQuery, redis: Redis, ticket_api: TicketAPI):
    try:
        tickets = await ticket_api.get_all_tickets(ticket_status="open")
        if not tickets:
            await call.message.edit_text(
                text="На данный момент все тикеты закрыты :)",
                reply_markup=create_inline_keyboard(width=1, ticket_management="Назад")
            )
            return
        tickets_str = json.dumps(tickets)
        await redis.set(name=f"open_tickets_{call.from_user.id}", value=tickets_str)

        page = 1
        total_pages = len(tickets)
        ticket = tickets[page - 1]
        message_text, keyboard = generate_ticket_message(ticket, page, total_pages, page_type="open_tickets")
        await call.message.edit_text(
            text=message_text,
            reply_markup=keyboard
        )
    except TelegramBadRequest:
        await call.answer("Обновлений не найдено")


@router.callback_query(PageNumber.filter(F.page_type == "open_tickets"))
async def open_tickets_pagination(call: CallbackQuery, callback_data: PageNumber, redis: Redis):
    await call.answer()
    action = callback_data.action
    if action == "current":
        return
    page = callback_data.page
    tickets = json.loads(await redis.get(name=f"open_tickets_{call.from_user.id}"))
    if action == "prev":
        page -= 1
    elif action == "next":
        page += 1

    ticket = tickets[page - 1]
    message_text, keyboard = generate_ticket_message(ticket, page, len(tickets), page_type="open_tickets")
    await call.message.edit_text(
        text=message_text,
        reply_markup=keyboard
    )
