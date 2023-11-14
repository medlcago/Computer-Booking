from datetime import datetime
from datetime import timezone

from aiogram import Router, F
from aiogram.types import BufferedInputFile
from aiogram.types import CallbackQuery

from keyboards.inline_utils import create_inline_keyboard
from utils.api_methods import BookingAPI
from utils.misc import create_bytes_excel_file

router = Router()


@router.callback_query(F.data == "bookings_list_excel")
async def bookings_list_excel(call: CallbackQuery, booking_api: BookingAPI):
    await call.answer(cache_time=15)
    bookings = await booking_api.get_all_computer_bookings()
    if bookings:
        headers = list(bookings[0].keys())
        file_bytes_xlsx = create_bytes_excel_file(data=bookings, headers=headers)
        file_name = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S") + "_bookings_list.xlsx"
        file = BufferedInputFile(file_bytes_xlsx, filename=file_name)
        await call.message.answer_document(
            document=file,
            caption=f"Список бронирований",
            reply_markup=create_inline_keyboard(width=1, close="❌ Закрыть")
        )
    else:
        await call.message.answer(f"Не удалось получить информацию о бронированиях")
