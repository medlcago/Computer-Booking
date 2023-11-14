from datetime import datetime
from datetime import timezone

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from aiogram.types import CallbackQuery
from aiogram.types import Message

from states.admins import ComputerCategory
from utils.api_methods import ComputerAPI
from utils.misc import create_bytes_excel_file

router = Router()


@router.callback_query(F.data == "computer_list_by_category_excel")
async def computer_list_by_category(call: CallbackQuery, state: FSMContext):
    """
    Список компьютеров конкретной категории в формате Excel (1)
    """
    await call.answer(cache_time=60)
    await call.message.answer("Вы хотите получить список компьютеров конкретной категории. Пожалуйста, введите категорию (VIP или Regular)")
    await state.set_state(ComputerCategory.category)


@router.message(ComputerCategory.category)
async def computer_list_by_category(message: Message, state: FSMContext, computer_api: ComputerAPI):
    """
    Список компьютеров конкретной категории в формате Excel (2)
    """
    await state.clear()
    category = message.text
    computers: list[dict] = await computer_api.get_computers_by_category(category=category)
    if computers:
        headers = list(computers[0].keys())
        file_bytes_xlsx = create_bytes_excel_file(data=computers, headers=headers)
        file_name = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S") + f"_computer_{category}_list.xlsx"
        file = BufferedInputFile(file_bytes_xlsx, filename=file_name)
        await message.reply_document(file, caption=f"Список компьютеров категории <i>{category}</i>")
    else:
        await message.reply(f"Не удалось получить информацию о компьютерах категории <i>{category}</i>")
