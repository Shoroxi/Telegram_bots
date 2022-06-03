import asyncio
from sql import create_db
from loader import bot, storage
import loadconfig
from handlers import dp
from DZ_bot.handlers.users import testing


async def on_shutdown(dp):
    await bot.close()
    await storage.close()


async def on_startup(dp):
    await asyncio.sleep(3)
    # await create_db()
    await bot.send_message(loadconfig.__admin_id__, "Я запущен!")

testing.register_handlers(dp, testing.handlers_config)

if __name__ == '__main__':
    from aiogram import executor

    try:
        executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)
    except BaseException as exc:
        testing.log.exception(exc)
