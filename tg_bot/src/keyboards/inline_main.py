from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.callbackdata import TopUpBalance

main_menu_button = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Показать меню", callback_data="show_menu")
    ]
])


def main_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="👤 Мой профиль", callback_data="my_profile"),
            InlineKeyboardButton(text="💼 Мои заказы", callback_data="my_orders")
        ],
        [
            InlineKeyboardButton(text="Список доступных компьютеров", callback_data="computer_available_list"),
        ],
        [
            InlineKeyboardButton(text="Информация о всех компьютерах", callback_data="computer_list")
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


def admin_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Управление пользователями", callback_data="user_management")
        ],
        [
            InlineKeyboardButton(text="Управление компьютерами", callback_data="computer_management")
        ],
        [
            InlineKeyboardButton(text="Управление бронированиями", callback_data="booking_management")
        ],
        [
            InlineKeyboardButton(text="Управление платежами", callback_data="payment_management")
        ],
        [
            InlineKeyboardButton(text="❌ Закрыть", callback_data="close")
        ]
    ])

    return keyboard


def user_management_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Заблокировать", callback_data="block_user"),
            InlineKeyboardButton(text="Разблокировать", callback_data="unblock_user")
        ],
        [
            InlineKeyboardButton(text="Все пользователи [Excel]", callback_data="user_list_excel"),
            InlineKeyboardButton(text="Информация о пользователе", callback_data="info_about_user")
        ],
        [
            InlineKeyboardButton(text="Все бронирования пользователя [Excel]", callback_data="user_booking_history_excel")
        ],
        [
            InlineKeyboardButton(text="🔙 Вернуться в админ панель", callback_data="show_admin_menu")
        ],
        [
            InlineKeyboardButton(text="❌ Закрыть", callback_data="close")
        ]
    ])

    return keyboard


def computer_management_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить компьютер", callback_data="add_computer")
        ],
        [
            InlineKeyboardButton(text="Все компьютеры [Excel]", callback_data="computer_list_excel"),
        ],
        [
            InlineKeyboardButton(
                text="Компьютеры конкретной категории [Excel]",
                callback_data="computer_list_by_category_excel"
            )
        ],
        [
            InlineKeyboardButton(text="Удалить компьютер", callback_data="delete_computer")
        ],
        [
            InlineKeyboardButton(text="🔙 Вернуться в админ панель", callback_data="show_admin_menu")
        ],
        [
            InlineKeyboardButton(text="❌ Закрыть", callback_data="close")
        ]
    ])

    return keyboard


def booking_management_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Все бронирования [Excel]", callback_data="booking_list_excel")
        ],
        [
            InlineKeyboardButton(
                text="Все бронирования пользователя [Excel]",
                callback_data="user_booking_history_excel"
            )
        ],
        [
            InlineKeyboardButton(text="🔙 Вернуться в админ панель", callback_data="show_admin_menu")
        ],
        [
            InlineKeyboardButton(text="❌ Закрыть", callback_data="close")
        ]
    ])

    return keyboard


def payment_management_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="История платежей пользователя", callback_data="user_payment_history_excel")
        ],
        [
            InlineKeyboardButton(text="🔙 Вернуться в админ панель", callback_data="show_admin_menu")
        ],
        [
            InlineKeyboardButton(text="❌ Закрыть", callback_data="close")
        ]
    ])

    return keyboard
