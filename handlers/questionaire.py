from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.states import Create
from keyboards import kb
from keyboards.kb import profile
from keyboards.kb import created_request_inline

from data.database import WorkDB

from rich.console import Console

router = Router()
console = Console()

db = WorkDB("./data/main.db")

@router.message(F.text.lower() == "создать запрос")
async def fill_profile(message: Message, state: FSMContext):
    print("AOAOA")
    await state.set_state(Create.request_title)
    await message.answer(
        "Давай начнем!\nВведите тему вопроса",
    )


@router.message(Create.request_title)
async def fill_profile(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(Create.request_text)
    await message.answer(
        "Хорошо!\nТеперь введи текст своего запроса",
    )


@router.message(Create.request_text)
async def fill_profile(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await state.set_state(Create.request_tags)
    await message.answer(
        "Осталось немного.\nУкажи теги для своего запроса\n \nПример: <code>Программирование, Языки, Проблема</code>",
    )


@router.message(Create.request_tags)
async def fill_profile(message: Message, state: FSMContext):
    await state.update_data(tags=message.text)
    data = await state.get_data()
    await state.clear()
    request_title = data.get("title")
    request_text = data.get("text")
    request_tags = data.get("tags")
    try: 
        db.setRequest(f"{message.from_user.id}", f"{message.from_user.full_name}", f"@{message.from_user.username}", f"{request_title}", f"{request_text}", f"{request_tags}")
        await message.answer(
            f"<b>Ваш запрос успешно отправлен✅:</b>\n    💠тема:  <u>{request_title}</u>\n    •  {request_text}\n \n    Теги: <code>{request_tags}</code>", 
        )
    except Exception:
        console.print_exception(show_locals=True)
    
    

 





    