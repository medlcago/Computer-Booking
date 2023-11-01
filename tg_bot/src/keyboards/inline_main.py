from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.callbackdata import PageNumber


def generate_pagination_keyboard_builder(page: int, total_pages: int) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    if page > 1:
        builder.button(text="◀️", callback_data=PageNumber(action="prev", page=page))
        if page < total_pages:
            builder.button(text=f"{page}/{total_pages}", callback_data=PageNumber(action="current", page=page))

    if page < total_pages:
        builder.button(text="▶️", callback_data=PageNumber(action="next", page=page))

    return builder
