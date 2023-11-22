from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.callbackdata import PageNumber


def create_pagination_keyboard_builder(page: int, total_pages: int, page_type: str) -> InlineKeyboardBuilder:
    kb_builder = InlineKeyboardBuilder()

    if page > 1:
        kb_builder.button(text="◀️", callback_data=PageNumber(action="prev", page=page, page_type=page_type))
        if page < total_pages:
            kb_builder.button(text=f"{page}/{total_pages}",
                              callback_data=PageNumber(action="current", page=page, page_type=page_type))

    if page < total_pages:
        kb_builder.button(text="▶️", callback_data=PageNumber(action="next", page=page, page_type=page_type))

    return kb_builder


def create_inline_keyboard(width: int,
                           *args: str,
                           last_btn: dict | None = None,
                           **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=button,
                callback_data=button
            ))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))

    kb_builder.row(*buttons, width=width)
    if last_btn:
        for button, text in last_btn.items():
            kb_builder.row(InlineKeyboardButton(
                text=text,
                callback_data=button
            ))
    return kb_builder.as_markup()
