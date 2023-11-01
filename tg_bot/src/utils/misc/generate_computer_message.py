from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.callbackdata import ComputerBooking
from keyboards.inline_main import generate_pagination_keyboard_builder


def generate_computer_message(computer: dict, page: int, total_pages: int) -> tuple[str, InlineKeyboardMarkup]:
    keyboard = generate_pagination_keyboard_builder(page, total_pages)
    keyboard.row(InlineKeyboardButton(
        text="Забронировать",
        callback_data=ComputerBooking(computer_id=computer.get("computer_id")).pack())
    )

    computer_info = f"""<b>Бренд:</b> {computer.get('brand')}
<b>Модель:</b> {computer.get("model")}
<b>Процессор:</b> {computer.get("cpu")}
<b>RAM:</b> {computer.get("ram")} ГБ
<b>SSD:</b> {computer.get("storage")} ГБ
<b>Видеокарта:</b> {computer.get("gpu")}
<b>Категория компьютера:</b> {computer.get("category")}
"""

    return computer_info, keyboard.as_markup()
