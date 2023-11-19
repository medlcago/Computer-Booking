from aiogram import Router, F
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import ErrorEvent, Message
from aiohttp import ClientConnectorError

router = Router()


@router.error(ExceptionTypeFilter(ClientConnectorError), F.update.message.as_("message"))
async def client_connector_error(event: ErrorEvent, message: Message):
    await message.reply("<b>Удаленный компьютер отклонил это сетевое подключение!</b>")
