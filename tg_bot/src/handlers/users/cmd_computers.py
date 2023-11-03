from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline_main import PageNumber
from utils.api_methods import ComputerAPI
from utils.misc import generate_computer_message

router = Router()


@router.callback_query(F.data == "computer_list")
async def command_computers(call: CallbackQuery, computer_api: ComputerAPI, state: FSMContext):
    computers = await computer_api.get_all_computers()
    if not computers:
        await call.message.edit_text("На данный момент доступных компьютеров нет.")
        return
    await state.update_data(computers=computers)

    page = 1
    total_pages = len(computers)
    computer = computers[page - 1]
    message_text, keyboard = generate_computer_message(computer, page, total_pages)
    await call.message.edit_text(text=message_text, reply_markup=keyboard)


@router.callback_query(PageNumber.filter())
async def computers_pagination(call: CallbackQuery, callback_data: PageNumber, state: FSMContext):
    await call.answer()
    action = callback_data.action
    if action == "current":
        return
    page = callback_data.page
    computers = (await state.get_data()).get("computers")
    if action == "prev":
        page -= 1
    elif action == "next":
        page += 1

    computer = computers[page - 1]
    message_text, keyboard = generate_computer_message(computer, page, len(computers))
    await call.message.edit_text(text=message_text, reply_markup=keyboard)
