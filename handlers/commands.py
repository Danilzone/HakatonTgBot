from aiogram  import Router, F
from aiogram.types import Message
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


@router.message(F.text.lower() == "запросы")
async def cmd_refund(message: Message):
    await message.reply(f"выберите один пункт",
                        reply_markup=kb.requests)


@router.message(F.text.lower() == "рейтинговая таблица")
async def cmd_refund(message: Message):
    await message.reply(f"выберите один пункт",
                        reply_markup=kb.answer)


@router.message()
async def cmds(message: Message):
    msg = message.text.lower()

    if msg == "на главный экран":
         await message.reply(f"выберите один пункт",
                     reply_markup=kb.main)

    elif msg == "личный кабинет":
        await message.reply(f"выберите один пункт",
                            reply_markup=kb.office)    

    elif msg == "запросы":
        await message.reply(f"выберите один пункт",
                          reply_markup=kb.requests)

    elif msg == "рейтинговая таблица":
        await message.reply(f"выберите один пункт",
                            reply_markup=kb.answer)
    
    elif msg == "мои запросы":
        try:
            res_db = db.getRequests(message.from_user.id)[1]
            print(res_db)
            await message.reply(f"выберите свой запрос", reply_markup=my_requests(res_db) )
        except Exception:
            console.print_exception(show_locals=True)