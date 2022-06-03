from marshmallow import Schema, fields, validate, post_load, ValidationError
import json
import os
import argparse
from telebot import types
import telebot


# Пример использование аргументов также можно увидиеть в loadconfig -
# parser = argparse.ArgumentParser()
# parser.add_argument("example")
# args = parser.parse_args()
#
# if args.example == 'Hello':
#     print('Welcome')
# else:
#     print("!")

# ---------------------------------
save_path = os.getcwd() + r"\JSON\Save.json"
print("\n" + save_path)

# ---------------------------------
# конструктор


class User(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

# __repr__, чтобы мы легко могли вывести экземпляр для проверки
    def __repr__(self):
        return f' {self.name}, мне {self.age}'

    def toJSON(self):
        return UserSchema().dumps(self, default=lambda o: o.__dict__,
            sort_keys=False, indent=4)


class UserSchema(Schema):
    name = fields.String(missing='Unknown', default='Unknown', valdiate=validate.Length(min=1)) # Дает дефолт значения
    age = fields.Integer(required=True, error_messages={'required': 'Введите ваш пол.'}, validate=validate.Range(min=0, max=None)) #  обязательно заполнить

# @post_load опциональная. Она нужна для загрузки схемы в качестве экземпляра какого-либо класса.
# Следовательно, в нашем случае она нужна для генерации экземпляров User.
# Метод make реализует экземпляр с помощью атрибутов.
    @post_load
    def make(self, data, **kwargs):
        return User(**data)

# ---------------------------------
# Открываем файл настройек, загружаем в конструктор, валидация


def Schema_load(file, action):
    with open(file, action) as f:
        try:
            data2 = UserSchema().load(json.load(f))
        except ValidationError as e:
            print(f'\nError Msg: {e.messages}')
            print(f'Valid Data: {e.valid_data}')
        return data2


# print("\n" + str(Schema_load("JSON/Te.json", "r")) + " - ЭТО НАСТРОЙКИ")
#
# print("\n" + str(Schema_load(save_path, "r")) + " - ЭТО СТАРЫЕ ДАННЫЕ\n")

#
# @dp.message_handler(commands=["bry"])
# async def reg_last(message):
#         chat_id = message.chat.id
#         name = await db.get_uname()
#         age = await db.get_age()
#         user = User(name, age)  # Даем значения
#         user_data = (user.toJSON())  # преобразовали в JSON, а его в dict
#         # eval = str -> json
#         user_schema = UserSchema().load(eval(user_data))
#         user_dump = UserSchema().dump(user_schema)
#
#         # Пищем в файл
#         with open(save_path, 'w') as outfile:
#             json.dump(user_dump, outfile)
#
#         # Открываем
#         with open(save_path) as json_file:
#             users = json.load(json_file)
#             print(users)
#
#         await bot.send_message(chat_id, f'Nice to meet you {name}\n Age: {str(age)}')
