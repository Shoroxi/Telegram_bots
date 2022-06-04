from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import executor

from DZ_bot.handlers.users import handlers

try:
    from loadconfig import __telegramtoken__, __admin_id__
except ImportError:
    exit('set TELEGRAM_TOKEN + ADMIN_ID')

bot = Bot(token=__telegramtoken__, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def on_shutdown(*args):
    await bot.close()
    await storage.close()


async def on_startup(*args):
    """Оповещение админа о запуске бота"""
    handlers.log.info('Бот запущен')
    await bot.send_message(chat_id=__admin_id__, text='Бот запущен')

handlers.register_handlers(dp, handlers.handlers_config)

if __name__ == '__main__':
    try:
        executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)
    except BaseException as exc:
        handlers.log.exception(exc)
