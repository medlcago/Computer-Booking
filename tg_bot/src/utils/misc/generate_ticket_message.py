from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.callbackdata import Ticket
from keyboards.inline_utils import create_pagination_keyboard_builder


def generate_ticket_message(
        ticket: dict,
        page: int,
        total_pages: int,
        page_type: str | None = None) -> tuple[str, InlineKeyboardMarkup]:
    ticket_id = ticket.get("id")
    title = ticket.get("title")
    assigned_to = ticket.get("assigned_to")
    status = ticket.get("status")
    created_at = ticket.get("created_at")
    updated_at = ticket.get("updated_at")

    if page_type is None:
        keyboard = InlineKeyboardBuilder()
    else:
        keyboard = create_pagination_keyboard_builder(page, total_pages, page_type=page_type).copy()

    if status == "open":
        keyboard.row(InlineKeyboardButton(
            text=f"✍️ Ответить",
            callback_data=Ticket(ticket_id=ticket_id, assigned_to=assigned_to).pack()),
        )

    if page_type is not None:
        keyboard.row(InlineKeyboardButton(
            text="🔄 Обновить данные",
            callback_data="open_tickets"
        ))

        keyboard.row(InlineKeyboardButton(
            text="Назад",
            callback_data="ticket_management")
        )
    else:
        keyboard.row(InlineKeyboardButton(
            text="❌ Закрыть",
            callback_data="close")
        )

    ticket_info = f"""<b>ID:</b> {ticket_id}
<b>Заголовок:</b> {title}
<b>Отправил:</b> {assigned_to}
<b>Статус:</b> {status}
<b>Создан:</b> {created_at}
<b>Обновлен:</b> {updated_at}
"""

    return ticket_info, keyboard.as_markup()
