from datetime import datetime, timezone

from aiogram import Router, F
from aiogram.types import BufferedInputFile
from aiogram.types import CallbackQuery

from filters import IsAdmin
from utils.api_methods import UserAPI
from utils.misc import create_bytes_excel_file

router = Router()


@router.callback_query(F.data == "user_list", IsAdmin())
async def user_list(call: CallbackQuery, user_api: UserAPI):
    await call.answer(cache_time=60)
    users: list[dict] = await user_api.get_all_users()
    if users:
        headers = list(users[0].keys())
        file_bytes_xlsx = create_bytes_excel_file(data=users, headers=headers)
        file_name = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S") + "_user_list.xlsx"
        file = BufferedInputFile(file_bytes_xlsx, filename=file_name)
        await call.message.answer_document(file, caption="Список пользователей")
    else:
        await call.message.answer("Не удалось получить информацию о пользователях")
