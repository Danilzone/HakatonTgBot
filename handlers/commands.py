from aiogram  import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject, CommandStart

from keyboards import kb
from rich import print
from data.database import WorkDB

from keyboards.kb import my_requests
from rich.console import Console

db = WorkDB("./data/main.db")

router = Router()

console = Console()


@router.message(CommandStart())
async def start(message : Message):
    await message.answer(f"Hi <b>{message.from_user.full_name}</b>", reply_markup=kb.main)

    # db.setUser(message.from_user.id, message.from_user.full_name, "@" + message.from_user.username)    
    # db.setRequest(message.from_user.id, message.from_user.full_name, "@" + message.from_user.username, "Майнинг", "Как в питоне сделать майнер?")
    # db.getRequests()


@router.message(F.text.lower() == "на главный экран")
async def cmd_refund(message: Message):
    await message.reply(f"выберите один пункт",
                        reply_markup=kb.main)


@router.message(F.text.lower() == "личный кабинет")
async def cmd_refund(message: Message):
    await message.reply(f"выберите один пункт",
                        reply_markup=kb.office)


@router.message(F.text.lower() == "мои запросы")
async def cmd_refund(message: Message):
    try:
        res_db = db.getRequests(message.from_user.id)[1]
        await message.reply(f"выберите свой запрос", reply_markup=my_requests(res_db) )
    except Exception:
        console.print_exception(show_locals=True)


@router.message(F.text.lower() == "запросы")
async def cmd_refund(message: Message):
    await message.reply(f"выберите один пункт",
                        reply_markup=kb.requests)


@router.message(F.text.lower() == "рейтинговая таблица")
async def cmd_refund(message: Message):
    await message.reply(f"выберите один пункт",
                        reply_markup=kb.answer)


# Тут мы получаем инфу с инлайн кнопок и выводим из бд нужный 'запрос'

@router.callback_query(F.data[:4] == "REQ ")
async def callback(call: CallbackQuery):
    print(call.data[4:])
    request = db.getRequest(call.from_user.id, call.data[4:])
    await callback.answer("Загрузка")
    await call.message.answer(f"💠тема: <u>{request[0]}</u>\n• {request[1]}", reply_markup=kb.interact_request)


# @router.message()
# async def cmds(message: Message):
#     msg = message.text.lower()
#     if msg == "на главный экран":
#          await message.reply(f"выберите один пункт",
#                      reply_markup=kb.main)

#     elif msg == "личный кабинет":
#         await message.reply(f"выберите один пункт",
#                             reply_markup=kb.office)    

#     elif msg == "запросы":
#         await message.reply(f"выберите один пункт",
#                           reply_markup=kb.requests)

#     elif msg == "рейтинговая таблица":
#         await message.reply(f"выберите один пункт",
#                             reply_markup=kb.answer)
    
#     elif msg == "мои запросы":
#         try:
#             res_db = db.getRequests(message.from_user.id)[1]
#             await message.reply(f"выберите свой запрос", reply_markup=my_requests(res_db) )
#         except Exception:
#             console.print_exception(show_locals=True)


"""
Работа с БД

db.getRequest(юзер_id, id_запроса)  -> получить статью пользователя 
db.getRequests(юзер_id)             -> получить все статьи пользователя 

db.setRequest(юзер_id, имя_юзера, собачка_юзера, заголовок_запроса, текст_запроса)            -> добавить статью 

"""