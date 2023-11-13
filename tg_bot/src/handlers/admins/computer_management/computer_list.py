from datetime import datetime
from datetime import timezone

from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile

from utils.api_methods import ComputerAPI
from utils.misc import create_bytes_excel_file

router = Router()


@router.callback_query(F.data == "computer_list")
async def computer_list(call: CallbackQuery, computer_api: ComputerAPI):
    """
    Список всех компьютеров в формате Excel
    """
    await call.answer(cache_time=60)
    computers: list[dict] = await computer_api.get_all_computers()
    if computers:
        headers = list(computers[0].keys())
        file_bytes_xlsx = create_bytes_excel_file(data=computers, headers=headers)
        file_name = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S") + "_computer_list.xlsx"
        file = BufferedInputFile(file_bytes_xlsx, filename=file_name)
        await call.message.answer_document(file, caption="Список компьютеров")
    else:
        await call.message.answer("Не удалось получить информацию о компьютерах")
