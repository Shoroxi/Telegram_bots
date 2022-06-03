import telebot
import loadconfig
tg = telebot.TeleBot(loadconfig.__telegramtoken__)

def get_name(message):
    msg = "Привет," + message.text
    tg.send_message(chat_id=message.chat.id, text=msg)

def get_age(message):
    msg = "Привет," + message.text
    tg.send_message(chat_id=message.chat.id, text=msg)

def get_text_messages(bot, message):
    ms_text = message.text

    if ms_text == "1":
        def_msg = 'Введите ваше имя\n'
        bot.register_next_step_handler(def_msg, get_name)


    elif ms_text == "2":
        age = int(input("Сколько вам лет\n"))
        tg.send_message(chat_id=message.chat.id, text=str(age))

    elif ms_text == "3":
        name = input('Введите ваше имя\n')
        spam = name * 5
        tg.send_message(chat_id=message.chat.id, text=spam)

    elif ms_text == "4":
        name = input('Введите ваше имя\n')
        age = int(input("Сколько вам лет\n"))
        tg.send_message(chat_id=message.chat.id, text=spam)

    elif ms_text == "5":
        age = int(input("Сколько вам лет\n"))
        if age >= 18:
            tg.send_message(chat_id=message.chat.id, text="Что ты здесь делаешь ты же старик\n")
        elif age < 18:
            tg.send_message(chat_id=message.chat.id, text='Ты еще мал, чтобы читать это\n')

    elif ms_text == "6":
        name = input('Введите ваше имя\n')
        msg = ""
        msg += (name[2:-1])
        msg += (name[::-1])
        msg += (name[:3])
        msg += (name[5:])
        tg.send_message(chat_id=message.chat.id, text=msg)

    elif ms_text == "7":
        # 7
        age = int(input("Сколько вам лет\n"))
        # Делаем Список
        A = 1  # Срез
        result = []
        for i in range(0, len(str(age)), A):
            result.append(int(str(age)[i: i + A]))
        tg.send_message(chat_id=message.chat.id, text="\nЛист : " + str(result))

        # Перебираем значения листа -> плюсуем, множим
        div = 1
        sm = 0

        for i in result:
            div = div * i
            sm = sm + i
        msg = ('\nСумма=' + str(sm) + '\nПроизведение =' + str(div))
        tg.send_message(chat_id=message.chat.id, text=msg)

    elif ms_text == "8":
        # 8
        tg.send_message(chat_id=message.chat.id, text='Введите ваше имя\n')
        print(name.upper())
        print(name.lower())
        print(name.capitalize())  # or name.title()
        U = name.capitalize()
        print(U.swapcase())
        tg.send_message(chat_id=message.chat.id, text=spam)

    elif ms_text == "9":
        # 9
        while True:
            try:
                name = input('Введите ваше имя\n')
                age = int(input("Сколько вам лет\n"))

                if (age < 1) or (age > 150):
                    tg.send_message(chat_id=message.chat.id, text="ГОДА")
                    raise ValueError
                elif not (name.isalpha()) and (name.isspace()):
                    tg.send_message(chat_id=message.chat.id, text="ИМЯ")
                    raise ValueError
                else:
                    tg.send_message(chat_id=message.chat.id, text="Тогда в безду списка его!\n")
                    break
            except ValueError as err:
                continue

    elif ms_text == "10":
        # 10
        math_z = int(input("\nСколько будет 2*2+2\n"))
        if math_z == 6:
            tg.send_message(chat_id=message.chat.id, text="Мда, я ответа тоже не знаю")
        else:
            tg.send_message(chat_id=message.chat.id, text="Дурачок, я тоже кстати")
