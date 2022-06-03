import os
import json

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=False, indent=4)

me = Object()
me.name = input("Введите имя\n")

# ---------------------------------
# Проверка файла
file = input("Путь к файлу\n")
if os.path.exists(file):
    me.f = "Y"
else:
    me.f = "N"

# ---------------------------------
# Удалить файл?
DEL = input("Удалить файл?")
if DEL == "да":
    os.remove(file)
    me.dl = "Y"
else:
    print("Как хочешь")
    me.dl = "N"

# ---------------------------------
# Вывод
print(me.toJSON())