import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from config import config
from handlers import admins
from handlers import cancel_handler_router
from handlers import close_handler_router
from handlers import errors
from handlers import unknown_action_router
from handlers import users
from middlewares import UserRegistrationMiddleware
from utils.api_methods import UserAPI, ComputerAPI, BookingAPI, PaymentAPI


async def main():
    bot = Bot(token=config.tg.token, parse_mode="html")
    storage = RedisStorage.from_url(config.redis.url)

    dp = Dispatcher(storage=storage)

    dp.include_router(cancel_handler_router)
    dp.include_router(close_handler_router)

    dp.include_router(admins.command_admin_router)
    dp.include_router(admins.user_management_router)
    dp.include_router(admins.user_list_router)
    dp.include_router(admins.info_about_user_router)
    dp.include_router(admins.info_about_user_bookings_router)

    dp.include_router(users.command_start_router)
    dp.include_router(users.show_main_menu_router)
    dp.include_router(users.show_my_profile_router)
    dp.include_router(users.top_up_balance_router)
    dp.include_router(users.computer_available_list_router)
    dp.include_router(users.computer_list_router)
    dp.include_router(users.show_my_orders_router)
    dp.include_router(users.computer_booking_router)

    dp.include_router(errors.error_handler_router)

    dp.include_router(unknown_action_router)

    dp.message.middleware(UserRegistrationMiddleware())

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S')
    logging.info(f"Bot running in {'DEBUG' if config.debug else 'RELEASE'} mode!")

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot,
                               user_api=UserAPI(base_url=config.api.base_url, api_key=config.api.api_key),
                               computer_api=ComputerAPI(base_url=config.api.base_url, api_key=config.api.api_key),
                               booking_api=BookingAPI(base_url=config.api.base_url, api_key=config.api.api_key),
                               payment_api=PaymentAPI(base_url=config.api.base_url, api_key=config.api.api_key),
                               config=config
                               )
    except Exception as ex:
        logging.error(f"[!!! Exception] - {ex}", exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
