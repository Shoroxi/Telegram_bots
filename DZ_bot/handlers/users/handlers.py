# from asyncpg import Connection, Record
# from asyncpg.exceptions import UniqueViolationError

import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters import Text

from aiogram.utils import markdown as md
from aiogram.types import ParseMode
from random import sample
from datetime import datetime, timedelta
from generate_ticket import draw_ticket

from DZ_bot.config.cities import CITIES_AND_FLIGHT_TIME as SFT
from DZ_bot.states.states import Steps

from DZ_bot import create_db

import random
from DZ_bot.Homework.marshmallow_homework import User, UserSchema
import os
import json


# =============== LOGGING ======================
import logging
log = logging.getLogger('DZ_bot')


def configure_logging(log):
    """Настройка логирования"""
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %H:%M'))
    stream_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler('aviaticketbot_messages.log', encoding='utf8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%d/%m/%Y %H:%M'))
    file_handler.setLevel(logging.INFO)

    if log.hasHandlers():
        log.handlers.clear()

    log.addHandler(stream_handler)
    log.addHandler(file_handler)

    log.setLevel(logging.INFO)


configure_logging(log)

# =============== START|HELP|CANCEL ======================

async def send_welcome(message: types.Message, state: FSMContext):
    """Ответ на команду /start"""
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await create_db.delete_user(message.chat.id)
    log.info(f'{message.chat.first_name} подключился к боту. ID {message.chat.id}\n')
    await message.reply(f'Привет {message.chat.first_name}! Я бот AirTicketLaggyBot.',
                        reply_markup=types.ReplyKeyboardRemove())
    await message.answer(f'Я создан для обработки заказов на авиарейсы.')
    await message.answer(f'Доступные команды: /ticket, /help, /cancel')


async def send_help(message: types.Message):
    await message.answer(f'Я бот AirTicketLaggyBot. Доступные команды: /start, /ticket, /help, /cancel')


async def cancel_command(message: types.Message, state: FSMContext):
    """Ответ на команду /cancel"""
    current_state = await state.get_state()
    if current_state is None:
        return
    log.debug('Отмена состояний %r', current_state)
    await state.finish()
    await message.answer('Отменено.', reply_markup=types.ReplyKeyboardRemove())
    await create_db.delete_user(message.chat.id)

# =============== СЦЕНАРИЙ ======================
async def reg_start(message: types.Message, state: FSMContext):
    """Ответ на команду /reg"""
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await create_db.delete_user(message.chat.id)
    log.debug('Начат сценарий')
    await state.set_state(Steps.city_from)
    await message.answer('Введите имя', reply_markup=types.ReplyKeyboardRemove())
    await create_db.create_user(message.chat.id, message.chat.username, 'Имя')





# =============== CMD ======================


class DBCommands:
    # =============== DATABASE - Posteg ======================
    pool: Connection = db
    ADD_NEW_USER = "INSERT INTO users(chat_id, username, full_name) VALUES ($1, $2, $3) RETURNING id"

    COUNT_USERS = "SELECT COUNT(*) FROM users"

    GET_ID = "SELECT id FROM users WHERE chat_id = $1"
    GET_UNAME = "SELECT uname FROM users WHERE chat_id = $1"
    GET_AGE = "SELECT age FROM users WHERE chat_id = $1"

    CHECK_BALANCE = "SELECT balance FROM users WHERE chat_id = $1"
    CHECK_REGS = "SELECT regit FROM users WHERE chat_id = $1"

    MARK_REGS = "UPDATE users SET regit=true WHERE chat_id = $1"
    ADD_MONEY = "UPDATE users SET balance=balance+$1 WHERE chat_id = $2"
    SET_AGE = "UPDATE users SET age=$1 WHERE chat_id = $2"
    SET_UNAME = "UPDATE users SET uname=$1 WHERE chat_id = $2"

    async def add_new_user(self):
        user = types.User.get_current()

        chat_id = user.id
        username = user.username
        full_name = user.full_name
        args = chat_id, username, full_name

        command = self.ADD_NEW_USER

        try:
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            pass

    async def count_users(self):
        record: Record = await self.pool.fetchval(self.COUNT_USERS)
        return record

    # =============== GET ======================
    async def get_id(self):
        command = self.GET_ID
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)

    async def get_uname(self):
        command = self.GET_UNAME
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)

    async def get_age(self):
        command = self.GET_AGE
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)

    # =============== CHECK ======================
    async def check_balance(self):
        command = self.CHECK_BALANCE
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)

    async def check_reg(self):
        command = self.CHECK_REGS
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)

    # =============== ADD ======================
    async def add_money(self, money):
        command = self.ADD_MONEY
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, money, user_id)

    async def add_reg(self):
        command = self.MARK_REGS
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)

    async def set_age(self, age):
        command = self.SET_AGE
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, age, user_id)

    async def set_uname(self, uname):
        command = self.SET_UNAME
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, uname, user_id)


db = DBCommands()

# =============== REGISTER ======================


async def register_user(message: types.Message, state: FSMContext):
    """Ответ на команду /start"""
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        # await models.delete_user(message.chat.id)
    chat_id = message.from_user.id
    id = await db.add_new_user()
    count_users = await db.count_users()
    reg = await db.check_reg()
    text = ""
    if not id:
        id = await db.get_id()
    else:
        text += "Записал в базу! "

    uname = await db.get_uname()
    age = await db.get_age()
    balance = await db.check_balance()
    text += f"""
Привет {uname}, тебе {age}
Сейчас в базе {count_users} человек!

Ваш баланс: {balance} монет.
{reg}

Добавить монет: /add_money

"""

    await bot.send_message(chat_id, text)


@dp.message_handler(commands=["blank"])
async def check_user_reg(message: types.Message):
    chat_id = message.from_user.id

    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    text = ""

    data = await state.get_data()
    answer1 = data.get("name")
    answer2 = data.get("age")

    reg = await db.check_reg()
    if reg == True and answer1 != None and answer2 != None:

        text += f"""
            Ваше имя: {answer1}
            Ваш возраст: {answer2}
            """

        await bot.send_message(chat_id, text)
    else:
        await enter_test(message)


@dp.message_handler(commands=["add_money"])
async def add_money(message: types.Message):
    random_amount = random.randint(1, 100)
    await db.add_money(random_amount)
    balance = await db.check_balance()

    text = f"""
Вам было добавлено {random_amount} монет.
Теперь ваш баланс: {balance}
    """
    await message.answer(text)


# =============== TESTING ======================


@dp.message_handler(Command("test"), state=None)
async def enter_test(message: types.Message):
    await message.answer("Вы начали тестирование.\n"
                         "Вопрос №1. \n\n"
                         "Ваше имя "
                         "(бесцельно блуждаете по интернету, клацаете пультом телевизора, просто смотрите в потолок)?")

    # Вариант 1 - с помощью функции сет
    await Test.Q1.set()


@dp.message_handler(state=Test.Q1)
async def name(message: types.Message, state: FSMContext):
    answer = message.text

    # Ваирант 2 получения state
    # state = dp.current_state(chat=message.chat.id, user=message.from_user.id)

    # Вариант 2 - передаем как словарь
    await state.update_data(
        {"uname": answer}
    )

    await message.answer("Вопрос №2. \n\n"
                         "Ваш возраст?")


    await Test.next()


@dp.message_handler(state=Test.Q2)
async def age(message: types.Message, state: FSMContext):
    # Достаем переменные
    data = await state.get_data()
    answer1 = data.get("uname") # name
    answer2 = message.text # age

    await state.update_data(
        {"uname": answer1, "age": answer2}
    )

    await db.add_reg() # Уже зареган
    await db.set_uname(str(answer1))
    await db.set_age(int(answer2))
    await message.answer("Спасибо за ваши ответы!")
    # await state.finish()
    await state.reset_state(with_data=False)     # Вариант завершения 3 - без стирания данных в data

# =============== File ======================
save_path = r"C:/Users/mspox/Desktop/STD_TgBot-main/DZ_bot/Homework/JSON/Te.json"


class FileDetector:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4)


FD = FileDetector()


@dp.message_handler(commands=["Save"])
async def save_json(message: types.Message):
        chat_id = message.chat.id
        name = await db.get_uname()
        age = await db.get_age()
        user = User(name, age)  # Даем значения
        user_data = (user.toJSON())  # преобразовали в JSON, а его в dict
        # eval = str -> json
        user_schema = UserSchema().load(eval(user_data))
        user_dump = UserSchema().dump(user_schema)

        # Пищем в файл
        with open(save_path, 'w') as outfile:
            json.dump(user_dump, outfile)

        # Открываем
        with open(save_path) as json_file:
            users = json.load(json_file)
            print(users)

        FD.name = name

        await bot.send_message(chat_id, f'Файл успешно сохранен! Имя: {name}\n Возраст: {str(age)}')


@dp.message_handler(commands=["exist"], state=None)
async def Qfile_path(message: types.Message):

    await message.answer('Введи Путь к файлу:\n')
    await File.File_Ex.set()


@dp.message_handler(state=File.File_Ex)
async def file_path(message: types.Message, state: FSMContext):
    file = message.text
    print(file)
    FD.filepath = file
    if os.path.exists(file):
        await state.update_data(
            {"file": file}
        )
        print(file)
        await File.QDel.set()
    else:
        await bot.send_message(message.chat.id, "Не нашел, отрубаю сценарий")
        await state.finish()


@dp.message_handler(state=File.QDel)
async def QDelff(message: types.Message):
    await message.answer("Удалить файл?\n")
    await File.Delete.set()


@dp.message_handler(state=File.Delete)
async def delete(message: types.Message, state: FSMContext):
    answer = message.text
    data = await state.get_data()
    file = data.get("file")
    if answer == "да":
        os.remove(file)
        FD.deleted = "Yes"
        await bot.send_message(message.chat.id, "Удалил")

    else:
        FD.deleted = "NO"
        await bot.send_message(message.chat.id, "Как хочешь")

    await state.finish()


def register_handlers(_dp, config):
    """Регистрация обработчиков"""

    for command_info in config['command_handlers']:
        _dp.register_message_handler(command_info[0], commands=command_info[1], state=command_info[2])
        _dp.register_message_handler(command_info[0], command_info[3], state=command_info[2])

    for communicate_info in config['communicate_handlers']:
        _dp.register_message_handler(communicate_info[0], state=communicate_info[1])

    for handler_info in config['state_handlers']:
        _dp.register_message_handler(handler_info[0], handler_info[1], state=handler_info[2])

handlers_config = {

    'command_handlers': (
        (send_welcome, 'start', '*', Text(equals='/start', ignore_case=True)),
        (send_help, 'help', '*', Text(equals='/help', ignore_case=True)),
        (cancel_command, 'cancel', '*', Text(equals='/cancel', ignore_case=True)),
        (reg_start, 'reg', '*', Text(equals='/reg', ignore_case=True)),
    ),

    'communicate_handlers': (
        (send_help, None),
    ),

    'state_handlers': [
        (name, lambda message: message.text.title() in SFT.keys(), Steps.city_from),

    ]
}


# =============== 1 HOMEWORK ======================


# @dp.message_handler(commands=["1"], state=DZ.T1)
# async def first (message: types.Message, state: FSMContext):
#     await message.answer("Привет, как звать")
#     name = message.text
#     await state.update_data(
#         {"name": name}
#     )
#     data = await state.get_data()
#     print(data)
#
# # @dp.message_handler(commands=["1"], state=DZ.Show)
# # async def show (message: types.Message, state: FSMContext):
#
#
# @dp.message_handler(commands=["1"], state=DZ.T2)
# async def first(message: types.Message, state: FSMContext):
#     elif ms_text == "2":
#         await message.answer("Сколько вам лет\n")
#         tg.send_message(chat_id=message.chat.id, text=str(age))

# @dp.message_handler(commands=["1"], state=DZ.T1)
# async def first(message: types.Message, state: FSMContext):
#     elif ms_text == "3":
#         name = input('Введите ваше имя\n')
#         spam = name * 5
#         tg.send_message(chat_id=message.chat.id, text=spam)
#
# @dp.message_handler(commands=["1"], state=DZ.T1)
# async def first(message: types.Message, state: FSMContext):
#     elif ms_text == "4":
#         name = input('Введите ваше имя\n')
#         age = int(input("Сколько вам лет\n"))
#         tg.send_message(chat_id=message.chat.id, text=spam)
#
# @dp.message_handler(commands=["1"], state=DZ.T1)
# async def first(message: types.Message, state: FSMContext):
#     elif ms_text == "5":
#         age = int(input("Сколько вам лет\n"))
#         if age >= 18:
#             tg.send_message(chat_id=message.chat.id, text="Что ты здесь делаешь ты же старик\n")
#         elif age < 18:
#             tg.send_message(chat_id=message.chat.id, text='Ты еще мал, чтобы читать это\n')
#
# @dp.message_handler(commands=["1"], state=DZ.T1)
# async def first(message: types.Message, state: FSMContext):
#     elif ms_text == "6":
#         name = input('Введите ваше имя\n')
#         msg = ""
#         msg += (name[2:-1])
#         msg += (name[::-1])
#         msg += (name[:3])
#         msg += (name[5:])
#         tg.send_message(chat_id=message.chat.id, text=msg)
#
# @dp.message_handler(commands=["1"], state=DZ.T1)
# async def first(message: types.Message, state: FSMContext):
#     elif ms_text == "7":
#         # 7
#         age = int(input("Сколько вам лет\n"))
#         # Делаем Список
#         A = 1  # Срез
#         result = []
#         for i in range(0, len(str(age)), A):
#             result.append(int(str(age)[i: i + A]))
#         tg.send_message(chat_id=message.chat.id, text="\nЛист : " + str(result))
#
#         # Перебираем значения листа -> плюсуем, множим
#         div = 1
#         sm = 0
#
#         for i in result:
#             div = div * i
#             sm = sm + i
#         msg = ('\nСумма=' + str(sm) + '\nПроизведение =' + str(div))
#         tg.send_message(chat_id=message.chat.id, text=msg)
#
# @dp.message_handler(commands=["1"], state=DZ.T1)
# async def first(message: types.Message, state: FSMContext):
#     elif ms_text == "8":
#         # 8
#         tg.send_message(chat_id=message.chat.id, text='Введите ваше имя\n')
#         print(name.upper())
#         print(name.lower())
#         print(name.capitalize())  # or name.title()
#         U = name.capitalize()
#         print(U.swapcase())
#         tg.send_message(chat_id=message.chat.id, text=spam)
#
# @dp.message_handler(commands=["1"], state=DZ.T1)
# async def first(message: types.Message, state: FSMContext):
#     elif ms_text == "9":
#         # 9
#         while True:
#             try:
#                 name = input('Введите ваше имя\n')
#                 age = int(input("Сколько вам лет\n"))
#
#                 if (age < 1) or (age > 150):
#                     tg.send_message(chat_id=message.chat.id, text="ГОДА")
#                     raise ValueError
#                 elif not (name.isalpha()) and (name.isspace()):
#                     tg.send_message(chat_id=message.chat.id, text="ИМЯ")
#                     raise ValueError
#                 else:
#                     tg.send_message(chat_id=message.chat.id, text="Тогда в безду списка его!\n")
#                     break
#             except ValueError as err:
#                 continue
#
#     elif ms_text == "10":
#         # 10
#         math_z = int(input("\nСколько будет 2*2+2\n"))
#         if math_z == 6:
#             tg.send_message(chat_id=message.chat.id, text="Мда, я ответа тоже не знаю")
#         else:
#             tg.send_message(chat_id=message.chat.id, text="Дурачок, я тоже кстати")
#
#
