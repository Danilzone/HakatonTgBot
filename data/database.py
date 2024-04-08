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


    # Отправка и получение 'запросов'  

    def setRequest(self, user_id, user_name, user_dogname, request_title, request_text):

        self.user_id = user_id
        self.user_name = user_name
        self.user_dogname = user_dogname
        
        self.user_id = user_id
        self.user_name = user_name
        self.user_dogname = user_dogname

        self.request_title = request_title
        self.request_text = request_text
        
        # Проверка на то, есть ли такая статья уже

        try:
            self.c.execute('INSERT INTO `requests` ("user_id", "user_name", "user_dogname", "request_title", "request_text") VALUES (?, ?, ?, ?, ?)', (user_id, user_name, user_dogname, request_title, request_text,))
            self.conn.commit()
            print(f"Запрос [green bold]'{request_title}'[/green bold] добавлен успешно!")
        
        except Exception:
            console.print_exctption(show_locals=True)


    def getRequests(self, user_id):
        self.user_id = user_id
        titles = self.c.execute(' SELECT "id", "request_title" FROM `requests` WHERE "user_id" = ? ', (user_id,)).fetchall()
        self.conn.commit()
      
        try:
            full_requests = self.c.execute(f' SELECT * FROM `requests` WHERE "user_id" = ? ', (user_id,)).fetchall()
            self.conn.commit()
            
            return full_requests, titles
        except Exception:
            console.print_exctption(show_locals=True) 


    def getRequest(self, user_id, request_id):
        self.user_id = user_id
        self.request_id = request_id
        try:
                request = self.c.execute(' SELECT "request_title", "request_text" FROM `requests` WHERE "id"= ? AND "user_id" = ? ',(request_id, user_id,)).fetchall()
                self.conn.commit()
                title = request[0][0]
                text = request[0][1]
                return title, text 
        
        except Exception:
            console.print_exctption(show_locals=True) 
    

    # Редактирование существующего 'запроса' и его удаление

    def editRequest(self, request_id, user_id, request_title, request_text):
        self.request_id = request_id
        self.user_id = user_id

        self.request_title = request_title
        self.request_text = request_text

        
        self.c.execute('UPDATE `requests` SET "request_title" = ?, "request_text" = ? WHERE id = ? AND user_id = ?', (request_id, user_id, request_title, request_text))
    
    
    def deletRequest(self, user_id, request_id):
        self.user_id = user_id
        self.request_id = request_id
        
        self.c.execute('DELETE FROM requests WHERE id = ? AND user_id = ?')
        self.conn.commit()
        


    def deletRequest(self, request_id, user_id):
        self.request_id = request_id
        self.user_id = user_id

    

# ТЕСТИРОВАНИЕ

# db = WorkDB("main.db")
# print(
# print(db.getRequest("1270679070", 6)[1])
# )
# db.setRequest("1270679070", "D_123", "@D_123UwU", "Дота", "текмт текстовый")
