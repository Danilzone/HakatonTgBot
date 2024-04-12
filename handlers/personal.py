
import ast
from aiogram  import Router, F, types
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, CommandObject, CommandStart

from aiogram.fsm.context import FSMContext
from utils.states import GetReqEdit
from utils.states import Form, Search,SearchByTags, SetAnswer, EditMyAnswer, Create

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

    db.setUser(message.from_user.id, message.from_user.full_name, "@" + message.from_user.username)    
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


@router.message(F.text.lower() == "мои ответы")
async def my_answers(message: Message):
    try:
        res_db = db.getMyAnswers(message.from_user.id)
        print(res_db)
        if not res_db:
            await message.answer("Вы еще не отвечали ни на какие запросы")
        else:
            for my_answer in res_db:
                await message.answer(f"💠<u>тема</u>: {my_answer[1]}\n • <u>Ваш ответ</u>: {my_answer[2]}\n", reply_markup=kb.interact_answer(my_answer[0]))
    except Exception:
        console.print_exception(show_locals=True)


@router.message(F.text.lower() == "рейтинговая таблица")
async def cmd_refund(message: Message):
    await message.reply(f"выберите один пункт",
                        reply_markup=kb.answer)



# Тут мы получаем инфу с инлайн кнопок и выводим из бд нужный 'запрос'


@router.message(F.text.lower() == "создать запрос")
async def fill_profile(message: Message, state: FSMContext):
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
