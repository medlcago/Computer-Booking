import json

from aiogram import Router, F
from aiogram.fsm.storage.redis import Redis
from aiogram.types import CallbackQuery

from keyboards.callbackdata import PageNumber
from keyboards.inline_utils import create_inline_keyboard
from utils.api_methods import ComputerAPI
from utils.misc import generate_computer_message

router = Router()


@router.callback_query(F.data == "computer_available_list")
async def computer_available_list(call: CallbackQuery, computer_api: ComputerAPI, redis: Redis):
    computers = await computer_api.get_all_computers(is_reserved=False)
    if not computers:
        await call.message.edit_text(
            text="На данный момент доступных компьютеров нет.",
            reply_markup=create_inline_keyboard(width=1, show_menu="Назад")
        )
        return
    available_computers_str = json.dumps(computers)
    await redis.set(name=f"available_computers_{call.from_user.id}", value=available_computers_str)

    page = 1
    total_pages = len(computers)
    computer = computers[page - 1]
    message_text, keyboard = generate_computer_message(computer, page, total_pages,
                                                       page_type="available_computers",
                                                       add_booking=True)
    await call.message.edit_text(
        text=message_text,
        reply_markup=keyboard
    )


@router.callback_query(PageNumber.filter(F.page_type == "available_computers"))
async def available_computers_pagination(call: CallbackQuery, callback_data: PageNumber, redis: Redis):
    await call.answer()
    action = callback_data.action
    if action == "current":
        return
    page = callback_data.page
    computers = json.loads(await redis.get(name=f"available_computers_{call.from_user.id}"))
    if action == "prev":
        page -= 1
    elif action == "next":
        page += 1

    computer = computers[page - 1]
    message_text, keyboard = generate_computer_message(computer, page, len(computers),
                                                       page_type="available_computers",
                                                       add_booking=True)
    await call.message.edit_text(text=message_text, reply_markup=keyboard)
