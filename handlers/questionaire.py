from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.states import Form
from keyboards.kb import profile
from keyboards.kb import rmk

router = Router()


@router.message(F.text.lower() == "создать запрос")
async def fill_profile(message: Message, state: FSMContext):
    await state.set_state(Form.request_title)
    await message.answer(
        "Давай начнем!\nВведите тему вопроса",
    )

