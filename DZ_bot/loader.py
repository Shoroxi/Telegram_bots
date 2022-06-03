import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from DZ_bot.sql import create_pool

from DZ_bot import loadconfig

bot = Bot(token=loadconfig.__telegramtoken__, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

# logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
#                     level=logging.INFO,
#                     )



loop = asyncio.get_event_loop()

db = loop.run_until_complete(create_pool())
