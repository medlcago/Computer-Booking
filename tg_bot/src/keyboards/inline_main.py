from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.callbackdata import PageNumber, TopUpBalance


def generate_pagination_keyboard_builder(page: int, total_pages: int, page_type: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    if page > 1:
        builder.button(text="◀️", callback_data=PageNumber(action="prev", page=page, page_type=page_type))
        if page < total_pages:
            builder.button(text=f"{page}/{total_pages}", callback_data=PageNumber(action="current", page=page, page_type=page_type))

    if page < total_pages:
        builder.button(text="▶️", callback_data=PageNumber(action="next", page=page, page_type=page_type))

    return builder


main_menu_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Показать меню", callback_data="show_menu")
    ]
])


def generate_inline_keyboard(callback_data: str, text: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=text, callback_data=callback_data)
        ]
    ])

    return keyboard


def main_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👤 Мой профиль", callback_data="my_profile")
        ],
        [
            InlineKeyboardButton(text="Список компьютеров", callback_data="computer_list"),
            InlineKeyboardButton(text="Мои заказы", callback_data="my_orders")
        ],
        [
            InlineKeyboardButton(text="💲 Пополнить баланс", callback_data="top_up_balance")
        ]
    ])

    return keyboard


def top_up_amount() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💵 100 рублей", callback_data=TopUpBalance(amount=100).pack()),
            InlineKeyboardButton(text="💵 300 рублей", callback_data=TopUpBalance(amount=300).pack())
        ],
        [
            InlineKeyboardButton(text="💵 1000 рублей", callback_data=TopUpBalance(amount=1000).pack()),
        ],
        [
            InlineKeyboardButton(text="Вернуться в меню", callback_data="show_menu")
        ]
    ])

    return keyboard
