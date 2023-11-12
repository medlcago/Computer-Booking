from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def unknown_action(message: Message) -> None:
    await message.reply("I don't understand you :(")
