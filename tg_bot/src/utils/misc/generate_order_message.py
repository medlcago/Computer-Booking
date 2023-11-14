from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline_utils import create_pagination_keyboard_builder


def generate_order_message(order: dict, page: int, total_pages: int) -> tuple[str, InlineKeyboardMarkup]:
    order_id = order.get("id")
    computer_id = order.get("computer_id")
    start_time = datetime.strptime(order.get("start_time"), "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d.%m.%Y %H:%M:%S")
    end_time = datetime.strptime(order.get("end_time"), "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%d.%m.%Y %H:%M:%S")

    keyboard = create_pagination_keyboard_builder(page, total_pages, page_type="orders").copy()
    keyboard.row(InlineKeyboardButton(
        text="📃 Скачать Excel файл",
        callback_data="my_orders_excel"
    ))
    keyboard.row(InlineKeyboardButton(
        text="Вернуться в меню",
        callback_data="show_menu")
    )

    order_info = f"""<b>ID заказа:</b> {order_id}
<b>ID компьютера:</b> {computer_id}
<b>Начало:</b> {start_time} UTC+0
<b>Конец:</b> {end_time} UTC+0
"""

    return order_info, keyboard.as_markup()
