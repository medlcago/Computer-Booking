from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_bot_commands(bot: Bot):
    ru_commands = [
        BotCommand(
            command="start",
            description="Запуск бота"
        ),
        BotCommand(
            command="bonus",
            description="Получить бонус"
        )
    ]

    await bot.set_my_commands(ru_commands, language_code="ru", scope=BotCommandScopeAllPrivateChats())
