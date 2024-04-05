from aiogram  import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart

from keyboards import *

router = Router()

@router.message(CommandStart())
async def start(message : Message):
    await message.answer(f"Hi <b>{message.from_user.full_name}</b>")



