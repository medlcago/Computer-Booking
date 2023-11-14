from datetime import datetime
from datetime import timezone

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from aiogram.types import CallbackQuery
from aiogram.types import Message

from filters import IsAdmin
from keyboards.inline_utils import create_inline_keyboard
from states.admins import UserBookingHistory
from utils.api_methods import BookingAPI
from utils.misc import create_bytes_excel_file

router = Router()


@router.callback_query(F.data == "user_booking_history_excel", IsAdmin())
async def user_booking_history_excel(call: CallbackQuery, state: FSMContext):
    """
    Информация о всех бронированиях пользователя (1)
    """
    await call.answer(cache_time=15)
    await call.message.answer("Вы хотите получить информацию о бронированиях пользователя.\nПожалуйста, введите его ID")
    await state.set_state(UserBookingHistory.user_id)


@router.message(UserBookingHistory.user_id)
async def user_booking_history_excel(message: Message, state: FSMContext, booking_api: BookingAPI):
    """
    Информация о всех бронированиях пользователя (2)
    """
    await state.clear()
    try:
        user_id = int(message.text)
    except ValueError:
        await message.reply(f"<i>ID</i> должен быть целым числом!")
        return

    bookings = await booking_api.get_computer_bookings_by_user_id(user_id=user_id)
    if bookings:
        headers = list(bookings[0].keys())
        file_bytes_xlsx = create_bytes_excel_file(data=bookings, headers=headers)
        file_name = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S") + "_user_bookings_list.xlsx"
        file = BufferedInputFile(file_bytes_xlsx, filename=file_name)
        await message.reply_document(
            document=file,
            caption=f"Информация о бронированиях <code>{user_id}</code>",
            reply_markup=create_inline_keyboard(width=1, close="❌ Закрыть")
        )
    else:
        await message.reply(f"Не удалось получить информацию о бронированиях пользователя <code>{user_id}</code>")
