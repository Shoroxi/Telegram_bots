from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from DZ_bot.states.states import Steps, File

from DZ_bot import create_db

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

    file_handler = logging.FileHandler('DZ_bot.log', encoding='utf8')
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
    await message.reply(f'Привет {message.chat.first_name}!', reply_markup=types.ReplyKeyboardRemove())
    await message.answer(f'Доступные команды: /reg, /save, /delete, /first_les, /help, /cancel')


async def send_help(message: types.Message):
    await message.answer(f'Доступные команды: /reg, /save, /delete, /first_les, /help, /cancel')


async def cancel_command(message: types.Message, state: FSMContext):
    """Ответ на команду /cancel"""
    current_state = await state.get_state()
    if current_state is None:
        return
    log.debug('Отмена состояний %r', current_state)
    await state.finish()
    await message.answer('Отменено.', reply_markup=types.ReplyKeyboardRemove())
    await create_db.delete_user(message.chat.id)

# =============== File Lesson №1 ======================


async def first_les(message: types.Message, state: FSMContext):
    """Ответ на команду /first_les"""

    await state.set_state(Steps.reg)
    current_state = await state.get_state()
    log.info('Cur state %r', current_state)

    async with state.proxy() as data:
        if data.get('name') == None:
            await state.finish()
            await message.answer('Зарегайся /reg', reply_markup=types.ReplyKeyboardRemove())
            await create_db.delete_user(message.chat.id)
            return
        else:
            log.debug(f'{data}')
            log.info(f'Проверка домашки первого урока\n')
            name = data["name"]
            age = int(data["age"])
            await message.answer(f'домашки первого урока', reply_markup=types.ReplyKeyboardRemove())
            await message.answer(f'№1. Имя: {name}')
            await message.answer(f'#2. Имя: {name}, Возраст: {age}')
            await message.answer(f'#3. Спам: {name*5}')
            await message.answer(f'#4. Какая-то шутка про Имя: {name}, Возраст: {age}')

            # 6 ------------------------ 6
            if age >= 18:
                await message.answer(f"#5 Что ты здесь делаешь ты же старик")
            elif age < 18:
                await message.answer(f'#5 Ты еще мал, чтобы читать это')

            msg = ""
            msg += f"\n{name[2:-1]}\n"
            msg += f"{name[::-1]}\n"
            msg += f"{name[:3]}\n"
            msg += f"{name[5:]}\n"
            await message.answer(f'#6. Имя: {msg}')
            # 7 ------------------------ 7
            # Делаем Список
            A = 1  # Срез
            result = []
            for i in range(0, len(str(age)), A):
                result.append(int(str(age)[i: i + A]))
            msg = "Лист : " + str(result)

            # Перебираем значения листа -> плюсуем, множим
            div = 1
            sm = 0

            for i in result:
                div = div * i
                sm = sm + i
            msg += '\nСумма=' + str(sm) + '\nПроизведение =' + str(div)
            await message.answer(f'#7. {msg}')

            # 8 ------------------------ 8
            msg = ""
            msg += f"\n{name.upper()}\n"
            msg += f"{name.lower()}\n"
            msg += f"{name.capitalize()}\n" # or name.title()
            U = name.capitalize()
            msg += f"{U.swapcase()}\n"
            await message.answer(f'#8. {msg}')

            # 9 ------------------------ 9
            while True:
                try:
                    if (age < 1) or (age > 150):
                        await message.answer("Возраст введен неверно")
                        raise ValueError
                    elif not (name.isalpha()) and (name.isspace()):
                        await message.answer("Имя введено неверно")
                        raise ValueError
                    else:
                        await message.answer("#9. Тогда в безду списка его!\n")
                        break
                except ValueError as err:
                    continue

            # 10 ------------------------ 10
            # math_z = int(input("\nСколько будет 2*2+2\n"))
            # if math_z == 6:
            #     tg.send_message(chat_id=message.chat.id, text="Мда, я ответа тоже не знаю")
            # else:
            #     tg.send_message(chat_id=message.chat.id, text="Дурачок, я тоже кстати")
            # await message.answer(f'#10. Тут ничего нету, тк надо отдельно в сценарий добавлять')
            # await state.finish()
            # await create_db.delete_user(message.chat.id)
            await state.set_state(Steps.math)
            await message.answer(f'#10. Сколько будет 2*2+2')


async def q_math(message: types.Message, state: FSMContext):
    """Ответ на #10"""

    await message.answer("Правильно")

    # await state.finish()
    await state.reset_state(with_data=False)


async def q_math_invalid(message: types.Message):
    """Не праавильно посчитал"""
    await message.answer('Неправильно')


# =============== СЦЕНАРИЙ РЕГИСТРИЦИИ ======================

async def reg_start(message: types.Message, state: FSMContext):
    """Ответ на команду /reg"""
    current_state = await state.get_state()
    if current_state is not None:
        log.info(f'Прочистим данные\n')
        await state.finish()
        await create_db.delete_user(message.chat.id)
    log.debug('Начат сценарий регистрации')

    # Ставим состояние
    # Спрашиваем
    # Суем в ДБ
    await state.set_state(Steps.name)
    await message.answer('Введите имя', reply_markup=types.ReplyKeyboardRemove())
    await create_db.create_user(message.chat.id, message.chat.username, 'Имя')


async def reg_name(message: types.Message, state: FSMContext):
    """Имя пользователя введен корректно"""
    # Суем в State
    async with state.proxy() as data:
        data['name'] = message.text
        log.debug(f'{data}')

    await state.set_state(Steps.age)
    await message.answer('Введите свой возраст', reply_markup=types.ReplyKeyboardRemove())
    await create_db.update_user(message.chat.id, 'Возраст')


async def reg_age(message: types.Message, state: FSMContext):
    """Возраст пользователя введен корректно"""
    async with state.proxy() as data:
        data['age'] = message.text
        data['reg'] = True
        await message.answer(f'Спасибо за регистрацию, {data["name"]}')

        log.debug(f'{data}')
        log.info(f'Имя: {data["name"]}')
        log.info(f'Возраст: {data["age"]}')
        log.info(f'Зареган: {data["reg"]}\n')

    # """Завершение сценария"""
    # await state.finish()
    await state.reset_state(with_data=False)
    # await create_db.delete_user(message.chat.id)
    # await create_db.update_user(message.chat.id, 'State:param')


async def reg_age_invalid(message: types.Message):
    """Количество мест выбрано некорректно"""
    await message.answer('Возраст задан неверно')

# =============== File Lesson №6.2 ======================


async def save_json(message: types.Message, state: FSMContext):
    """Ответ на команду /save"""
    log.debug('Начат сценарий сохранения файла')

    save_path = os.getcwd() + r"\handlers\users\JSON\Save.json"
    log.info(f"{save_path}")

    async with state.proxy() as data:
        user = User(data["name"], data["age"])  # Даем значения
        user_data = (user.toJSON())  # преобразовали в JSON, а его в dict
        # eval = str -> json
        user_schema = UserSchema().load(eval(user_data))
        user_dump = UserSchema().dump(user_schema)

        with open(save_path, 'w') as outfile:
            json.dump(user_dump, outfile)

        await message.answer(f'Файл успешно сохранен! \nИмя: {data["name"]} \n Возраст: {data["age"]}')

# =============== File Lesson №6.1 ======================


async def del_file_start(message: types.Message, state: FSMContext):
    """Ответ на команду /delete"""
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await create_db.delete_user(message.chat.id)
    log.debug('Начат сценарий удаления файла')

    await state.set_state(File.file_path)
    await message.answer('Введи Путь к файлу:\n', reply_markup=types.ReplyKeyboardRemove())
    await create_db.create_user(message.chat.id, message.chat.username, 'Путь к файлу')


async def file_path(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['file_path'] = message.text
        if os.path.exists(data['file_path']):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["Да", "Нет"]
            keyboard.add(*buttons)

            await message.answer("Удалить файл?\n", reply_markup=keyboard)
            await state.set_state(File.del_file)
            await create_db.update_user(message.chat.id, 'State:param')
        else:
            await message.answer("Не нашел, отрубаю сценарий", reply_markup=types.ReplyKeyboardRemove())
            await state.finish()


async def q_del(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['delete_answer'] = message.text
        log.debug(f'{data}')
        if data['delete_answer'] == "Да":
            os.remove(data['file_path'])
            await message.answer(f'Файл успешно удален! \nПуть к файлу: {data["file_path"]}', reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
        elif data['delete_answer'] == "Нет":
            await message.answer(f'Ладно, отрубаю сценарий! \nПуть к файлу: {data["file_path"]}', reply_markup=types.ReplyKeyboardRemove())
            await state.finish()
        else:
            await message.answer("Не понял", reply_markup=types.ReplyKeyboardRemove())

# =============== register_handlers ======================


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
        (save_json, 'save', '*', Text(equals='/save', ignore_case=True)),
        (del_file_start, 'delete', '*', Text(equals='/delete', ignore_case=True)),

        (first_les, 'first_les', '*', Text(equals='/first_les', ignore_case=True)),


    ),

    'communicate_handlers': (
        (send_help, None),
    ),

    'state_handlers': [
        (reg_name, lambda message: message.text, Steps.name),
        (reg_age, lambda message: all([message.text.isdigit(), message.text in [str(x) for x in range(1, 100)]]), Steps.age),
        (reg_age_invalid, lambda message: not all([message.text.isdigit(), message.text in [str(x) for x in range(1, 100)]]), Steps.age),
        (q_math_invalid, lambda message: message.text != "6", Steps.math),
        (q_math, lambda message: message.text == "6", Steps.math),

        (file_path, lambda message: message.text, File.file_path),
        (q_del, lambda message: message.text, File.del_file),
    ]
}
