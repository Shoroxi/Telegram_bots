import telebot
# Импортируем типы из модуля, чтобы создавать кнопки
from telebot import types
import random
import json

bot = telebot.TeleBot("5201655115:AAFbPgpEaPMThZCUETrvHZiHjqqnAbx1MoI")

ID = 0
HP = 1
WORD = 2
GUESS = 3
LETTERS = 4
CATEGORIES_PATH = 'JSON/categories.json'
CATEGORIES = {"ANIMALS": {"EN": 'Animals', "RU": 'Животные'}, "EAT": {"EN": 'Eat', "RU": 'Еда'},
              "HOUSE": {"EN": "House", "RU": "Дом"}, "CLOTHES": {"EN": "Clothes", "RU": "Вещи"},
              "SCHOOL": {"EN": "School", "RU": "Школа"}, "MUSIC": {"EN": "Music", "RU": "Музыка"},
              "PROFESSIONS": {"EN": "Professions", "RU": "Профессии"}, "PC": {"EN": "PC", "RU": "Компьютер"},
              "NATURE": {"EN": "Nature", "RU": "Природа"}, "SPORT": {"EN": "Sport", "RU": "Спорт"},
              "BODY": {"EN": "Body", "RU": "Человек"}}

###########################################################
# Бкувы для кнопок
#ABC = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'.split()
# релизовать игроку выбор языка
###########################################################

ABC = 'А Б В Г Д Е Ж З И Й К Л М Н О П Р С Т У Ф Х Ц Ч Ш Щ Ъ Ы Ь Э Ю Я'.split()
# Список с активными игроками
players = []


# Обработчик сообщений
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global players
    if message.text == "Играть" or message.text == "играть" or message.text == "/play":
        if player_founder(message)[HP] == 0:
            players.remove(player_founder(message))
            # Создаём кнопки
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            # Кнопки с категориями
            categories_words = [types.InlineKeyboardButton(text="Любая", callback_data="All"),
                                types.InlineKeyboardButton(text="Животные", callback_data="ANIMALS"),
                                types.InlineKeyboardButton(text="Еда", callback_data="EAT"),
                                types.InlineKeyboardButton(text="Дом", callback_data="HOUSE"),
                                types.InlineKeyboardButton(text="Одежда", callback_data="CLOTHES"),
                                types.InlineKeyboardButton(text="Школа", callback_data="SCHOOL"),
                                types.InlineKeyboardButton(text="Музыка", callback_data="MUSIC"),
                                types.InlineKeyboardButton(text="Тело", callback_data="BODY"),
                                types.InlineKeyboardButton(text="Спорт", callback_data="SPORT"),
                                types.InlineKeyboardButton(text="Компьютер", callback_data="PC"),
                                types.InlineKeyboardButton(text="Природа", callback_data="NATURE"),
                                types.InlineKeyboardButton(text="Профессии", callback_data="PROFESSIONS")]
            keyboard.add(*categories_words)
            bot.send_message(message.chat.id, 'Выбери категорию: ', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, 'Игра уже идёт, 🚫 - выход')
            bot.send_message(message.chat.id, "Тема: " + player_founder(message)[5])
            letters_buttons(message)
    elif message.text in player_founder(message)[LETTERS]:
        # Находи нашего игрока в списке players
        tmp_player = player_founder(message)
        # Удалить букву-кнопку
        tmp_player[LETTERS].remove(message.text)
        # Если игрок угадал
        if message.text in tmp_player[WORD]:
            guess_changer(message)
            if tmp_player[WORD] == tmp_player[GUESS]:
                keyboard = types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id, 'Ты выиграл 🥳', reply_markup=keyboard)
                bot.send_message(message.chat.id, 'Правильное слово - ' + ''.join(tmp_player[WORD]))
                players.remove(tmp_player)
            else:
                letters_buttons(message)
        # Если игрок ошибся
        else:
            if tmp_player[HP] <= 1:
                keyboard = types.ReplyKeyboardRemove()
                bot.send_message(message.chat.id, '💀')
                bot.send_message(message.chat.id, 'Ты проиграл 😞', reply_markup=keyboard)
                bot.send_message(message.chat.id, 'Правильное слово - ' + ''.join(tmp_player[WORD]))
                players.remove(tmp_player)
            else:
                tmp_player[HP] -= 1
                letters_buttons(message)
    elif message.text == "🚫️":
        # Убираем клавиатуру
        keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Выход', reply_markup=keyboard)
        players.remove(player_founder(message))
    else:
        print(message.text)



@bot.callback_query_handler(func=lambda call: True)
def get_callback(call):
    # Выбрана категория " "

    if call.data == "All":
        call.data = random.choice(CATEGORIES)

    if call.data in CATEGORIES:
        with open(CATEGORIES_PATH, "r", encoding="utf8") as read:
            word = list(random.choice(json.load(read)[call.data][0]))
            new_player(call.message, word, CATEGORIES[call.data]['RU'])


def new_player(message, word, theme):
    if player_founder(message)[HP] == 0:
        players.remove(player_founder(message)) #ID

        hp = 6
        guess = []
        letters = list(ABC)

        for i in range(0, len(word)):
            if not word[i] == '_':
                guess.append("_")
            else:
                guess.append(" ")
                word[i] = ' '

        # blanks = ''.join('_' if c.isalpha() else ch for ch in word)
        # or
        # blanks = re.sub('[A-Za-z]', '_', word)

        print(' '.join(word))
        print(' '.join(guess))


        player = [message.chat.id, hp, word, guess, letters, theme]
        # ID - 0, HP - 1, WORD - 2, GUESS - 3, LETTERS - 4
        bot.send_message(message.chat.id, "Тема: " + theme)

        players.append(player)
    else:
        bot.send_message(message.chat.id, 'Игра уже идёт, 🚫 - выход')
        bot.send_message(message.chat.id, "Тема: " + player_founder(message)[5])
    letters_buttons(message)


# Найти игрока по ID
def player_founder(message):
    while True:
        for player in players:
            if player[ID] == message.chat.id:
                return player
        players.append([message.chat.id, 0, [], [], []])
        print("Err")


def hp_visual(message):
    hp = player_founder(message)[HP]
    if hp > 0:
        with open('JSON/categories.json', "r", encoding="utf8") as read:
            if hp == 6:
                bot.send_message(message.chat.id, json.load(read)["FIRST_POSITION"])
            elif hp == 5:
                bot.send_message(message.chat.id, json.load(read)["SECOND_POSITION"])
            elif hp == 4:
                bot.send_message(message.chat.id, json.load(read)["THIRD_POSITION"])
            elif hp == 3:
                bot.send_message(message.chat.id, json.load(read)["FOURTH_POSITION"])
            elif hp == 2:
                bot.send_message(message.chat.id, json.load(read)["FIFTH_POSITION"])
            elif hp == 1:
                bot.send_message(message.chat.id, json.load(read)["SIXTH_POSITION"])

        tmp = []
        i = 1
        while i <= 6:
            tmp.append('[')
            if hp >= i:
                tmp.append('❤️')
            else:
                tmp.append('🖤')
            tmp.append('] ')
            i += 1
        bot.send_message(message.chat.id, ''.join(tmp))


# клавиатура для игры
def letters_buttons(message):
    # Готовим клавиатуру
    keyboard = types.ReplyKeyboardMarkup(row_width=7)
    # Список кнопок
    buttons_added = []
    # И добавляем в неё кнопки
    for letter in player_founder(message)[LETTERS]:
        tmp = types.KeyboardButton(letter)
        buttons_added.append(tmp)
    keyboard.add(*buttons_added, types.KeyboardButton("🚫️"))
    hp_visual(message)
    if not buttons_added == []:
        bot.send_message(message.chat.id, ' '.join(player_founder(message)[GUESS]), reply_markup=keyboard)

def guess_changer(message):
    tmp_player = player_founder(message)
    for i in range(0, len(tmp_player[WORD])):
        if message.text == tmp_player[WORD][i]:
            tmp_player[GUESS][i] = message.text


bot.polling(none_stop=True, interval=0)