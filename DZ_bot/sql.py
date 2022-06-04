# import asyncio
# import asyncpg
# import logging
#
# from DZ_bot import loadconfig
#
# logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
#                     level=logging.INFO, datefmt='%d/%m/%Y %H:%M')
#
# file_handler = logging.FileHandler('aviaticketbot_messages.log', encoding='utf8')
# file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %H:%M'))
# file_handler.setLevel(logging.INFO)
# log = logging.getLogger('avia_ticket_bot')
# log.addHandler(file_handler)
#
# DATABASE_URL = loadconfig.__database_url__
#
#
# async def create_db():
#     create_db_command = open("create_db.py", "r").read()
#
#     logging.info("Connecting to database...")
#     conn: asyncpg.Connection = await asyncpg.connect(DATABASE_URL)
#     await conn.execute(create_db_command)
#     await conn.close()
#     logging.info("Table users created")
#
#
# async def create_pool():
#     return await asyncpg.create_pool(DATABASE_URL)
#
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(create_db())
