
from menus import Menu, goto_menu

class Dice:
    """
    Класс игры в кости.
    """
    dice = [1, 2, 3, 4, 5, 6]
    # Обработчик нажатий на кнопки

    def __init__(self):
        self.computerChoice = self.__class__.getRandomDice()
        self.player1Choice = self.__class__.getRandomDice()

    @classmethod
    def getRandomDice(cls):
        # Бросаем кости
        lenValues = len(cls.dice)
        import random
        rndInd = random.randint(0, lenValues - 1)
        return cls.dice[rndInd]

    def playerChoice(self):
        winner = None
        if self.player1Choice == self.computerChoice:
            winner = "Ничья!"
        elif self.player1Choice > self.computerChoice:
            winner = "Игрок выиграл!"
        else:
            winner = "Компьютер выиграл!"
        return f"{self.player1Choice} vs {self.computerChoice} = " + winner


def get_text_messages(tg, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Стоп!" or ms_text == "Выйти" :

        goto_menu(tg, chat_id, "Выход")
        return


    elif ms_text == "Бросить кости":
        dc = Dice()
        text_game = dc.playerChoice()
        tg.send_message(chat_id, text=text_game)