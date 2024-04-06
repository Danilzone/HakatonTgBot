# работа с БД
from rich import print
from rich.console import Console

import sqlite3

console = Console()

class WorkDB:
    def __init__(self, way_db):

        self.conn = sqlite3.connect(way_db)    # подключаемся к базе данных
        self.c = self.conn.cursor()                 # Создаем курсор - для работы с бд

    def getTest(self):

        res = self.c.execute(' SELECT * FROM `users` ').fetchall()
        self.conn.commit()
        print("Получен из бд - " + res)

    def setTest(self, user_id, user_name, user_dogname):
        self.user_id = user_id
        self.user_name = user_name
        self.user_dogname = user_dogname

        try:
            res = self.c.execute(' INSERT INTO `users` ("user_id", "user_name", "user_dogname") VALUES (?, ?, ?) ', (user_id, user_name, user_dogname,))
            self.conn.commit()
            print("Юзер добален!")
            
        except Exception:
            console.print_exception(show_locals=True)


