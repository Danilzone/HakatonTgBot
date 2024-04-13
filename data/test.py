from database import WorkDB
from rich import print

db = WorkDB("main.db")

# db.rating()
# res = db.getMyAnswers(719833590)
print(db.getAnswers(1))
# print(db.getRequest(719833590, 41))

# print(res)