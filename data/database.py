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

    def setRequest(self, user_id, user_name, user_dogname, request_title, request_text, request_tags):

        self.user_id = user_id
        self.user_name = user_name
        self.user_dogname = user_dogname
        
        self.user_id = user_id
        self.user_name = user_name
        self.user_dogname = user_dogname

        self.request_title = request_title
        self.request_text = request_text
        self.request_tags = request_tags
        
        # Проверка на то, есть ли такая статья уже
        self.c.execute('INSERT INTO `requests` ("user_id", "user_name", "user_dogname", "request_title", "request_text", "request_tags") VALUES (?, ?, ?, ?, ?, ?)', (user_id, user_name, user_dogname, request_title, request_text, request_tags,))
        self.conn.commit()
        print(f"Запрос [green bold]'{request_title}'[/green bold] добавлен успешно!")
        



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
            request = self.c.execute(' SELECT "request_title", "request_text", "request_tags" FROM `requests` WHERE "id"= ? AND "user_id" = ? ',(request_id, user_id,)).fetchall()
            self.conn.commit()
            if not request:
                print("[red bold]В БД нет такой записи")
                return None
            
            title = request[0][0]
            text = request[0][1]
            tags = request[0][2]
            return title, text, tags 
        
        except Exception:
            console.print_exctption(show_locals=True) 
    

    # Редактирование существующего 'запроса' и его удаление

    def editRequest(self, user_id, request_title, request_text):
        self.user_id = user_id

        self.request_title = request_title
        self.request_text = request_text

        self.c.execute('UPDATE `requests` SET "request_title" = ?, "request_text" = ? WHERE id = ? AND user_id = ?', (request_title, request_text, user_id,))
        self.conn.commit()


    def editRequestTitle(self, user_id, request_id, request_title):
        self.user_id = user_id
        self.user_id = request_id
        self.request_title = request_title

        self.c.execute('UPDATE `requests` SET "request_title" = ? WHERE id = ? AND user_id = ?', (request_title, request_id, user_id,))
        self.conn.commit()


    def editRequestText(self, user_id, request_id, request_text):
        self.user_id = user_id
        self.user_id = request_id
        self.request_text = request_text

        self.c.execute('UPDATE `requests` SET "request_text" = ? WHERE id = ? AND user_id = ?', (request_text, request_id, user_id,))
        self.conn.commit()


    def editRequestTags(self, user_id, request_id, request_tags):
        self.user_id = user_id
        self.user_id = request_id
        self.request_tags = request_tags

        self.c.execute('UPDATE `requests` SET "request_tags" = ? WHERE id = ? AND user_id = ?', (request_tags, request_id, user_id,))
        self.conn.commit()
    
    
    def deleteRequest(self, request_id, user_id):
        self.user_id = user_id
        self.request_id = request_id
        
        self.c.execute('DELETE FROM `requests` WHERE id = ? AND user_id = ?', (request_id, user_id,))
        self.conn.commit()
        
        
     # создание, редактирование и удаление ответов на запросы
        
    def setAnswer(self, request_id, user_id, user_dogname, answer_text):
        self.request_id = request_id
        self.user_id = user_id
        self.user_dogname = user_dogname
        self.answer_text = answer_text
        try:
            self.c.execute('INSERT INTO `answer` (`request_id`, `user_id`, `user_dogname`, `answer_text`) VALUES (?, ?, ?, ?)', (request_id, user_id, user_dogname, answer_text,))
            self.conn.commit()
        except Exception:
            console.print_exctption(show_locals=True) 
            
    def deleteAnswer(self, answer_id, user_id):
        self.user_id = user_id
        self.answer_id = answer_id
        
        self.c.execute('DELETE FROM `answer` WHERE id = ? AND user_id = ?',(answer_id, user_id,))
        self.conn.commit()
    
    def editAnswer(self, answer_id, user_id, answer_text):
        self.answer_id = answer_id
        self.user_id = user_id
        self.answer_text = answer_text
        
        self.c.execute('UPDATE `answer` SET "answer_text" = ? WHERE id = ? AND user_id = ?',(answer_text, answer_id, user_id,))
        self.conn.commit()



        

# ТЕСТИРОВАНИЕ

db = WorkDB("main.db")

# db.setRequest("9009", "Asd", "@Asd", "qwert", "lorem lorem lorem lorem", "Tag tag tag")
# db.deleteRequest("8", "9009")
# db.getRequest("9009", "8")
# db.editRequestTags("9009", "9", "ew wdsf sgf")