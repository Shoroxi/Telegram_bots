import telebot
import menus
from menus import Menu

import loadconfig
tg = telebot.TeleBot(loadconfig.__telegramtoken__)
tg_group_id = loadconfig.__tg_group_id__
my_id = loadconfig.__my_id__

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# logger = telebot.logger
# logger.setLevel(logging.DEBUG)

@tg.message_handler(commands=['start'])
def command(message):
    chat_id = message.chat.id
    txt_message = f"Привет, {message.from_user.first_name}! Я тестовый бот для курса программирования на языке Python"
    tg.send_message(chat_id, text=txt_message, reply_markup=Menu.getMenu(chat_id, "Главное меню").markup)


@tg.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    subMenu = menus.goto_menu(tg, chat_id, ms_text)  # попытаемся использовать текст как команду меню, и войти в него
    if subMenu is not None:
        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды

        return  # мы вошли в подменю, и дальнейшая обработка не требуется

    cur_menu = Menu.getCurMenu(chat_id)
    if Menu.cur_menu is not None and ms_text in cur_menu.buttons:

        module = cur_menu.module

        if module != "":  # проверим, есть ли обработчик для этого пункта меню в другом модуле, если да - вызовем его (принцип инкапсуляции)
            exec(module + ".get_text_messages(tg, message)")

        elif ms_text == "Помощь":
            send_help(chat_id)
    else:  # ======================================= случайный текст
        tg.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
        menus.goto_menu(tg, chat_id, "Главное меню")

def goto_menu(chat_id, name_menu):
    if name_menu == "Выход" and Menu.cur_menu != None and Menu.cur_menu.parent != None:
        target_menu = Menu.getMenu(chat_id, Menu.cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(chat_id, name_menu)

    if target_menu != None:
        tg.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)
        return True
    else:
        return False


def send_help(chat_id):
    tg.send_message(chat_id, "хпфу")

# ============== Запуск🚀
if __name__ == '__main__':
    tg.polling(none_stop=True, interval=0) # bot.infinity_polling()
