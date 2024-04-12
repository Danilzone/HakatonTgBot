from database import WorkDB
from rich import print

db = WorkDB("main.db")


# res = db.topBestAnswers(15)
res = db.topWostAnswers(15)
print("    [red bold] От худшего\n")
for answer in res:
     print(f"Ответ от : [yellow]{answer[0][3]}[/yellow]\n- [green bold]{answer[0][4]} [/green bold]\nОценка [cyan bold]{answer[0][5]} [/cyan bold]\n")
