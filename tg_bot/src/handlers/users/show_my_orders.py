from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.callbackdata import PageNumber
from keyboards.inline_main import generate_inline_keyboard
from utils.api_methods import BookingAPI
from utils.misc import generate_order_message

router = Router()


@router.callback_query(F.data == "my_orders")
async def show_my_orders(call: CallbackQuery, booking_api: BookingAPI, state: FSMContext):
    user_id = call.from_user.id
    orders = await booking_api.get_computer_bookings_by_user_id(user_id=user_id)
    if not orders:
        await call.message.edit_text(
            text="Список ваших заказов пуст.",
            reply_markup=generate_inline_keyboard(callback_data="show_menu", text="Назад")
        )
        return
    await state.update_data(orders=orders)

    page = 1
    total_pages = len(orders)
    order = orders[page - 1]
    message_text, keyboard = generate_order_message(order, page, total_pages)
    await call.message.edit_text(
        text=message_text,
        reply_markup=keyboard
    )


@router.callback_query(PageNumber.filter(F.page_type == "orders"))
async def orders_pagination(call: CallbackQuery, callback_data: PageNumber, state: FSMContext):
    await call.answer()
    action = callback_data.action
    if action == "current":
        return
    page = callback_data.page
    orders = (await state.get_data()).get("orders")
    if action == "prev":
        page -= 1
    elif action == "next":
        page += 1

    order = orders[page - 1]
    message_text, keyboard = generate_order_message(order, page, len(orders))
    await call.message.edit_text(
        text=message_text,
        reply_markup=keyboard
    )
