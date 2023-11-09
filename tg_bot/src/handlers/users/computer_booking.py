from datetime import datetime
from datetime import timedelta
from datetime import timezone

from aiogram import Router
from aiogram.types import CallbackQuery

from keyboards.callbackdata import ComputerBooking
from keyboards.inline_main import generate_inline_keyboard
from templates.texts import COMPUTER_BOOKING
from utils.api_methods import BookingAPI
from utils.api_methods import ComputerAPI
from utils.api_methods import UserAPI

router = Router()


@router.callback_query(ComputerBooking.filter())
async def computer_booking(call: CallbackQuery,
                           callback_data: ComputerBooking,
                           user_api: UserAPI,
                           computer_api: ComputerAPI,
                           booking_api: BookingAPI
                           ):
    computer_id = callback_data.computer_id
    user_id = call.from_user.id

    computer = await computer_api.get_computer_by_id(computer_id=computer_id)
    total_cost = computer.get("price_per_hour")
    user = await user_api.get_user_by_id(user_id=user_id)

    if (current_balance := user.get("balance")) - total_cost >= 0:
        if not computer.get("is_reserved"):
            start_time = datetime.now(timezone.utc)
            end_time = datetime.now(timezone.utc) + timedelta(hours=1)

            if booking := (await booking_api.create_computer_booking(
                    user_id=user_id,
                    computer_id=computer_id,
                    start_time=start_time.isoformat(),
                    end_time=end_time.isoformat()
            )):
                if await user_api.update_user_details(user_id=user_id, balance=current_balance - total_cost):
                    await call.message.edit_text(
                        text=COMPUTER_BOOKING.format(
                            booking_id=booking.get("id"),
                            start_time=start_time.strftime("%d.%m.%Y %H:%M:%S"),
                            end_time=end_time.strftime("%d.%m.%Y %H:%M:%S")
                        )
                    )
                else:
                    await booking_api.delete_computer_booking(booking_id=booking.get("id"))
                    await call.message.edit_text("Произошла ошибка при бронировании компьютера.")
            else:
                await call.message.edit_text("Произошла ошибка при бронировании компьютера.")
        else:
            await call.message.answer(
                text="На данный момент компьютер недоступен.",
                reply_markup=generate_inline_keyboard(
                    callback_data="show_menu",
                    text="Вернуться в меню"
                )
            )
    else:
        await call.message.edit_text(
            text="На вашем балансе недостаточно средств. Пожалуйста, пополните баланс и повторите попытку.",
            reply_markup=generate_inline_keyboard(
                text="💲 Пополнить баланс",
                callback_data="top_up_balance"
            )
        )

    await call.answer(cache_time=60)
