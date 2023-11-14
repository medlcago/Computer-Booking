from datetime import datetime
from datetime import timezone

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from aiogram.types import CallbackQuery
from aiogram.types import Message

from keyboards.inline_utils import create_inline_keyboard
from states.admins import UserPaymentHistory
from utils.api_methods import PaymentAPI
from utils.misc import create_bytes_excel_file

router = Router()


@router.callback_query(F.data == "user_payment_history_excel")
async def user_payment_history_excel(call: CallbackQuery, state: FSMContext):
    """
    Информация о всех платежах пользователя (1)
    """
    await call.answer(cache_time=15)
    await call.message.answer("Вы хотите получить информацию о платежах пользователя.\nПожалуйста, введите его ID")
    await state.set_state(UserPaymentHistory.user_id)


@router.message(UserPaymentHistory.user_id)
async def user_payment_history_excel(message: Message, state: FSMContext, payment_api: PaymentAPI):
    """
    Информация о всех платежах пользователя (2)
    """
    await state.clear()
    try:
        user_id = int(message.text)
    except ValueError:
        await message.reply(f"<i>ID</i> должен быть целым числом!")
        return

    payments = await payment_api.get_user_payments(user_id=user_id)
    if payments:
        headers = list(payments[0].keys())
        file_bytes_xlsx = create_bytes_excel_file(data=payments, headers=headers)
        file_name = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S") + f"_{user_id}_payment_history.xlsx"
        file = BufferedInputFile(file_bytes_xlsx, filename=file_name)
        await message.reply_document(
            document=file,
            caption=f"Информация о платежах <code>{user_id}</code>",
            reply_markup=create_inline_keyboard(width=1, close="❌ Закрыть")
        )
    else:
        await message.reply(f"Не удалось получить информацию о платежах пользователя <code>{user_id}</code>")
