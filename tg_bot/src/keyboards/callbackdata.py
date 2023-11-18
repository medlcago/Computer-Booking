from aiogram.filters.callback_data import CallbackData


class PageNumber(CallbackData, prefix="page"):
    page_type: str
    action: str
    page: int


class ComputerBooking(CallbackData, prefix="booking"):
    computer_id: int


class TopUpBalance(CallbackData, prefix="top_up_balance"):
    amount: int


class Ticket(CallbackData, prefix="ticket"):
    ticket_id: int
    assigned_to: int
