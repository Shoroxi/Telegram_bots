import telebot
import wikipedia
from wikipedia import summary

import loadconfig
tg = telebot.TeleBot(loadconfig.__telegramtoken__)

wikipedia.set_lang("ru")


def process_definition(message):
    try:
        def_msg = str(message.text)
        def_str = summary(def_msg, sentences=10)
        def_split = def_str.split("\n\n", 1)[0]
        tg.send_message(chat_id=message.chat.id, text=def_msg + "\n\n" + def_split)
    except Exception:
        msg = "Не нашел!"
        tg.send_message(chat_id=message.chat.id, text=msg)


def get_text_messages(tg, message):
    ms_text = message.text

    if ms_text == "Поиск значения слова":
        def_msg = tg.reply_to(message, "Значение слова...")
        tg.register_next_step_handler(def_msg, process_definition)
