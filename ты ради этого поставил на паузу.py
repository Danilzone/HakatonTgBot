import time
import os
from rich.progress import Progress
os.system('cls||clear')
with Progress() as progress:

    task1 = progress.add_task("[yellow]Создание БД...", total=700)
    task2 = progress.add_task("[green bold]Сосздание бота...", total=740)
    task3 = progress.add_task("[cyan]Что-то еще ...", total=1000)

    while not progress.finished:
        progress.update(task1, advance=0.6)
        progress.update(task2, advance=0.2)
        progress.update(task3, advance=0.8)
        time.sleep(0.1)
