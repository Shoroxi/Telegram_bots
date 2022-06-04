from aiogram.dispatcher.filters.state import StatesGroup, State


class Steps(StatesGroup):
    name = State()
    age = State()
    reg = State()
    math = State()


class File(StatesGroup):
    file_path = State()

    del_file = State()

