from database import WorkDB
from rich import print

db = WorkDB("main.db")


db.dislike(4, 12222222)