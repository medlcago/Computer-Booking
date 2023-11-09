from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.callbackdata import ComputerBooking
from keyboards.inline_main import generate_pagination_keyboard_builder


def generate_computer_message(computer: dict, page: int, total_pages: int) -> tuple[str, InlineKeyboardMarkup]:
    brand = computer.get("brand")
    model = computer.get("model")
    cpu = computer.get("cpu")
    ram = computer.get("ram")
    storage = computer.get("storage")
    gpu = computer.get("gpu")
    category = computer.get("category")
    price_per_hour = computer.get("price_per_hour")

    keyboard = generate_pagination_keyboard_builder(page, total_pages, page_type="computers").copy()
    keyboard.row(InlineKeyboardButton(
        text=f"Забронировать [{price_per_hour}₽/час]",
        callback_data=ComputerBooking(computer_id=computer.get("computer_id")).pack()),
    )
    keyboard.row(InlineKeyboardButton(
        text="Вернуться в меню",
        callback_data="show_menu")
    )

    computer_info = f"""<b>Бренд:</b> {brand}
<b>Модель:</b> {model}
<b>Процессор:</b> {cpu}
<b>RAM:</b> {ram} ГБ
<b>SSD:</b> {storage} ГБ
<b>Видеокарта:</b> {gpu}
<b>Категория компьютера:</b> {category}
<b>Цена за час:</b> {price_per_hour} ₽
"""

    return computer_info, keyboard.as_markup()
