import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from config import load_config
from handlers.users import command_computers_router, command_start_router
from middlewares import UserRegistrationMiddleware
from utils.api_methods import UserAPI, ComputerAPI, BookingAPI


async def main():
    config = load_config(debug := True)
    bot = Bot(token=config.tg.token, parse_mode="html")
    storage = RedisStorage.from_url(config.redis.url)

    dp = Dispatcher(storage=storage)

    dp.include_router(command_start_router)
    dp.include_router(command_computers_router)

    dp.message.middleware(UserRegistrationMiddleware())

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S')
    logging.info(f"Bot running in {'DEBUG' if debug else 'RELEASE'} mode!")

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot,
                               user_api=UserAPI(base_url=config.api.base_url, api_key=config.api.api_key),
                               computer_api=ComputerAPI(base_url=config.api.base_url, api_key=config.api.api_key),
                               booking_api=BookingAPI(base_url=config.api.base_url, api_key=config.api.api_key))
    except Exception as ex:
        logging.error(f"[!!! Exception] - {ex}", exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
