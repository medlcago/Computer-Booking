from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

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


def main_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Список компьютеров", callback_data="computer_list")
        ],
        [
            InlineKeyboardButton(text="Мои заказы", callback_data="my_orders")
        ]
    ])

    return keyboard
