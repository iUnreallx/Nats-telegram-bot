import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv, find_dotenv

from core.admin import mailing
from core.database.postgres_connect import async_session
from core.handlers import start
from core.middleware.postgres_middleware import DbPostgresConnectMiddleware

load_dotenv(find_dotenv())

TOKEN = getenv("TOKEN")

async def main() -> None:
    await async_database_create()
    logging.basicConfig(level=logging.INFO)

    dp = Dispatcher()
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    postgres_database_middleware = DbPostgresConnectMiddleware(session_pool=async_session)
    add_to_postgres_middleware = DbPostgresConnectMiddleware(session_pool=async_session)

    dp.update.middleware(postgres_database_middleware)
    dp.update.middleware(add_to_postgres_middleware)

    dp.include_routers(
        start.router,
        mailing.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot polling stopped.')
