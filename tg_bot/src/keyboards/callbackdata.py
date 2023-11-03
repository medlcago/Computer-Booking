from aiogram.filters.callback_data import CallbackData


class PageNumber(CallbackData, prefix="page"):
    action: str
    page: int


class ComputerBooking(CallbackData, prefix="booking"):
    computer_id: int