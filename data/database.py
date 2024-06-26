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
        self.c.execute('INSERT INTO `requests` ("user_id", "user_name", "user_dogname", "request_title", "request_text", "request_lower_text", "request_lower_title","request_tags") VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (user_id, user_name, user_dogname, request_title, request_text, request_text.lower(), request_title.lower(), request_tags,))
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
            console.print_exception(show_locals=True) 


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
            console.print_exception(show_locals=True) 
    
    def getRequestById(self, request_id):
        self.request_id = request_id

        res = self.c.execute(' SELECT * FROM `requests` WHERE "id" = ? ', (request_id,)).fetchall()
        self.conn.commit()
        
        if not res:
            print("[red bold]В БД нет такой записи")
            print("[yellow bold]Видимо её удалили")
            return None
        id = res[0][0]
        user_id = res[0][1]
        user_name = res[0][2]
        user_dogname = res[0][3]
        request_title = res[0][4]
        request_text = res[0][5]
        request_tags = res[0][6]
        return id, user_id, user_name, user_dogname, request_title, request_text, request_tags 




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

            res = self.c.execute(' SELECT "user_id" FROM `requests` WHERE "id"  = ?  ', (request_id,)).fetchone()[0]
            self.conn.commit()
            return res
        
        except Exception:
            console.print_exception(show_locals=True) 
            
    def getAnswers(self, request_id ):            
        self.request_id = request_id

        res = self.c.execute(' SELECT * FROM `answer` WHERE "request_id" = ? ORDER BY "count_like" DESC ', (request_id,)).fetchall()
        self.conn.commit()
        
        if not res:
            print("[red bold]В БД нет такой записи")
            print("[yellow bold]Видимо её удалили")
            return None
        
        return res


    def getMyAnswers(self, user_id):
        self.user_id = user_id

        res = self.c.execute(' SELECT * FROM `answer` WHERE "user_id" = ? ', (user_id,)).fetchall()
        self.conn.commit()
        # print(res)
        answer=[]

        for my_answ in res:
            req_ans = self.c.execute(' SELECT "request_title" FROM `requests` WHERE "id" = ? ', (my_answ[1],)).fetchone()
            self.conn.commit()

            if req_ans:
                # print(req_ans[0])

                # print(f"\nТема: {req_ans[0]}\nВаш ответ: {my_answ[4]}\n")
                answer += [[my_answ[0],req_ans[0], my_answ[4]]]
        return answer


    def deleteAnswer(self, answer_id):
        self.answer_id = answer_id
        self.c.execute('DELETE FROM `answer` WHERE id = ? ', (answer_id,))
        self.conn.commit()
    

    def editAnswer(self, answer_id, user_id, answer_text):
        self.answer_id = answer_id
        self.user_id = user_id
        self.answer_text = answer_text
        
        self.c.execute('UPDATE `answer` SET "answer_text" = ? WHERE id = ? AND user_id = ?',(answer_text, answer_id, user_id,))
        self.conn.commit()


    def searchRequestText(self, find_text):
        self.find_text = find_text
        res = self.c.execute(f'SELECT "id","user_id", "user_dogname", "request_title", "request_text", "request_tags" FROM `requests` WHERE "request_lower_text" LIKE "%{find_text}%" COLLATE NOCASE OR "request_lower_title" LIKE "%{find_text}%" COLLATE NOCASE').fetchall()
        return res
        

    def searchRequestTags(self, find_text):
        self.find_text = find_text
        res = self.c.execute(f'SELECT "id","user_id", "user_dogname", "request_title", "request_text", "request_tags" FROM `requests` WHERE "request_tags" LIKE "%{find_text}%" COLLATE NOCASE OR "request_tags" LIKE "%{find_text}%" COLLATE NOCASE').fetchall()
        return res
        

    def like(self, answer_id, liked_user_id):
        self.answer_id = answer_id
        self.liked_user_id = liked_user_id

        check = self.c.execute(' SELECT * FROM `answer` WHERE "id" = ? ', (answer_id,)).fetchall()
        self.conn.commit()
        
        author_id = check[0][2]
        author_cont_like = int(self.c.execute('SELECT "likes" FROM `users` WHERE "user_id" = ? ', (author_id,)).fetchone()[0])
        self.conn.commit()
        

        if not check:
            return "No Find"

        list_likes = self.c.execute(' SELECT "list_likes" FROM `users` WHERE "user_id" = ? ', (liked_user_id,)).fetchone()
        self.conn.commit()


        if f"{answer_id}, " in list_likes[0]:
            print("Уже лайкнуто")
            return False

        else: 

                print("Оценено")
                list = self.c.execute(' SELECT "list_likes" FROM `users` WHERE "user_id" = ? ', (liked_user_id,)).fetchone()[0]
                self.conn.commit()

                new_list = list + f"{answer_id}, "

                count_like = int(self.c.execute(' SELECT "count_like" FROM `answer` WHERE "id" = ? ', (answer_id,)).fetchone()[0])  
                self.conn.commit()

                count_like += 1
                
                self.c.execute(' UPDATE `answer` SET "count_like" = ? WHERE "id" = ?', (count_like, answer_id,))
                self.conn.commit()    

                self.c.execute(' UPDATE `users` SET "list_likes" = ? WHERE "user_id" = ? ', (new_list, liked_user_id,))
                self.conn.commit()

                self.c.execute('UPDATE `users` SET "likes" = ? WHERE "user_id" = ? ', (author_cont_like + 1, author_id,))
                self.conn.commit()

                return True
            

    def dislike(self, answer_id, liked_user_id):
        self.answer_id = answer_id
        self.liked_user_id = liked_user_id

        check = self.c.execute(' SELECT * FROM `answer` WHERE "id" = ? ', (answer_id,)).fetchall()
        self.conn.commit()
        
        author_id = check[0][2]
        author_cont_like = int(self.c.execute('SELECT "likes" FROM `users` WHERE "user_id" = ? ', (author_id,)).fetchone()[0])
        self.conn.commit()

        if not check:
            return "No Find"

        list_likes = self.c.execute(' SELECT "list_likes" FROM `users` WHERE "user_id" = ? ', (liked_user_id,)).fetchone()
        self.conn.commit()


        if f"{answer_id}, " in list_likes[0]:
            print("уже лайкнуто - диз")
            return False

        else: 

            print("оценено дизом")
            list = self.c.execute(' SELECT "list_likes" FROM `users` WHERE "user_id" = ? ', (liked_user_id,)).fetchone()[0]
            self.conn.commit()

            new_list = list + f"{answer_id}, "

            count_like = int(self.c.execute(' SELECT "count_like" FROM `answer` WHERE "id" = ? ', (answer_id,)).fetchone()[0])  
            self.conn.commit()

            count_like -= 1
            
            self.c.execute(' UPDATE `answer` SET "count_like" = ? WHERE "id" = ?', (count_like, answer_id,))
            self.conn.commit()    

            self.c.execute(' UPDATE `users` SET "list_likes" = ? WHERE "user_id" = ? ', (new_list, liked_user_id,))
            self.conn.commit()

            self.c.execute('UPDATE `users` SET "likes" = ? WHERE "user_id" = ? ', (author_cont_like - 1, author_id,))
            self.conn.commit()

            return True


    def topBestAnswers(self, request_id):
        self.request_id = request_id
        res = self.c.execute(' SELECT * FROM `answer` WHERE "request_id" = ?  ORDER BY "count_like" DESC ', (request_id,) ).fetchall()
        self.conn.commit() 

        answers = []

        for answer in res:
            answers += [[answer]]
        
        return answers

    def topWostAnswers(self, request_id):
        self.request_id = request_id
        res = self.c.execute(' SELECT * FROM `answer` WHERE "request_id" = ?  ORDER BY "count_like" ASC ', (request_id,) ).fetchall()
        self.conn.commit() 

        answers = []

        for answer in res:
            answers += [[answer]]
        
        return answers   


    def rating(self):
        res = self.c.execute(' SELECT "user_dogname", "likes" "likes" FROM `users` ORDER BY "likes" DESC LIMIT 5 ').fetchall()
        self.conn.commit()

        return res
    
    def my_acc(self, user_id):
        self.user_id = user_id

        res = self.c.execute(' SELECT "likes" FROM `users` WHERE "user_id" = ? ', (user_id,)).fetchone()[0]
        self.conn.commit()
        
        count_anser = self.c.execute(' SELECT * FROM `answer` WHERE "user_id" = ? ', (user_id,)).fetchall()
        self.conn.commit()

        count_request = self.c.execute(' SELECT * FROM `requests` WHERE "user_id" = ? ', (user_id,)).fetchall()
        self.conn.commit()

        c_a = 0
        c_r = 0

        for ca in count_anser:
            c_a +=1

        for cr in count_request:
            c_r +=1


        return res, c_a, c_r