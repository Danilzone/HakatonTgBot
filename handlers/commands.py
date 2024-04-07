from aiogram  import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart

from keyboards import kb

from data.database import WorkDB

db = WorkDB("./data/main.db")

router = Router()

@router.message(CommandStart())
async def start(message : Message):
    await message.answer(f"Hi <b>{message.from_user.full_name}</b>", reply_markup=kb.main)

    # db.setUser(message.from_user.id, message.from_user.full_name, "@" + message.from_user.username)    
    # db.setRequest(message.from_user.id, message.from_user.full_name, "@" + message.from_user.username, "Майнинг", "Как в питоне сделать майнер?")
    # db.getRequests()
    
@router.message(F.text == "На главный экран")
async def cmd_refund(message: Message):
    await message.reply(f"выберите один пункт",
                        reply_markup=kb.main)


@router.message(F.text == "Личный кабинет")
async def cmd_refund(message: Message):
    await message.reply(f"выберите один пункт",
                        reply_markup=kb.office)


@router.message(F.text == "Запросы")
async def cmd_refund(message: Message):
    await message.reply(f"выберите один пункт",
                        reply_markup=kb.requests)


@router.message(F.text == "Рейтинговая таблица")
async def cmd_refund(message: Message):
    await message.reply(f"выберите один пункт",
                        reply_markup=kb.answer)