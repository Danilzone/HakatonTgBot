# работа с БД
from rich import print
from rich.console import Console

import sqlite3

console = Console()

class WorkDB:
    def __init__(self, way_db):
        self.way_db = way_db
        try:
            self.conn = sqlite3.connect(way_db)         # подключаемся к базе данных
            self.c = self.conn.cursor()                 # Создаем курсор - для работы с бд
            print("БД подключена")

        except Exception:
            console.print_exception(show_locals=True)
            
            
    def getUser(self):
        try: 
            res = self.c.execute(' SELECT * FROM `users` ').fetchall()
            self.conn.commit()
            print(res)
        except Exception:
            console.print_exception(show_locals=True)
            

    def setUser(self, user_id, user_name, user_dogname):
        self.user_id = user_id
        self.user_name = user_name
        self.user_dogname = user_dogname

        try:
            self.c.execute(' INSERT OR IGNORE INTO `users` ("user_id") VALUES (?) ', (user_id,))
            self.c.execute(' UPDATE `users` SET "user_name" = ?, "user_dogname" = ? WHERE "user_id" = ? ', (user_name, user_dogname, user_id ))
            self.conn.commit()
            print("Юзер добален!")
            
        except Exception:
            console.print_exception(show_locals=True)
            

    def setRequest(self, user_id, user_name, user_dogname, request_title, request_text):

        self.user_id = user_id
        self.user_name = user_name
        self.user_dogname = user_dogname
        
        self.user_id = user_id
        self.user_name = user_name
        self.user_dogname = user_dogname

        self.request_title = request_title
        self.request_text = request_text

        try:
            self.c.execute('INSERT INTO `requests` ("user_id", "user_name", "user_dogname", "request_title", "request_text") VALUES (?, ?, ?, ?, ?)', (user_id, user_name, user_dogname, request_title, request_text,))
            self.conn.commit()
            print(f"Запрос [green bold]'{request_title}'[/green bold] добавлен успешно!")
        
        except Exception:
            console.print_exctption(show_locals=True)


    def getRequests(self):
        try:
            res = self.c.execute(' SELECT * FROM `requests` ').fetchall()
            self.conn.commit()
            print(res)
        except Exception:
            console.print_exctption(show_locals=True) 
    
    