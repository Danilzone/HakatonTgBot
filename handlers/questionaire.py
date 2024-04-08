from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.states import Form
from keyboards import kb
from keyboards.kb import profile
from keyboards.kb import created_request_inline

router = Router()


@router.message(F.text.lower() == "создать запрос")
async def fill_profile(message: Message, state: FSMContext):
    print("AOAOA")
    await state.set_state(Form.request_title)
    await message.answer(
        "Давай начнем!\nВведите тему вопроса",
    )

@router.message(Form.request_title)
async def fill_profile(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(Form.request_text)
    await message.answer(
        "Хорошо!\nТеперь введи текст своего запроса",
    )

@router.message(Form.request_text)
async def fill_profile(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(Form.request_tags)
    await message.answer(
        "Осталось немного.\nУкажи теги для своего запроса\n \nПример: <code>Программирование, Языки, Проблема</code>",
    )


@router.message(Form.request_tags)
async def fill_profile(message: Message, state: FSMContext):
    await state.update_data(tags=message.text)
    data = await state.get_data()
    await state.clear()
    request_title = data.get("title")
    request_text = data.get("text")
    request_tags = data.get("tags")
    await message.answer(
        f"Вот твой запрос:\n    💠тема:  <u>{request_title}</u>\n    •  {request_text}\n \nТеги: <code>{request_tags}</code>", 
        reply_markup=kb.created_request_inline
    )

    