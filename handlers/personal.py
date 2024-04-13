
import ast
from aiogram  import Router, F, types
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, CommandObject, CommandStart

from aiogram.fsm.context import FSMContext
from utils.states import GetReqEdit
from utils.states import Form, Search,SearchByTags, SetAnswer, EditMyAnswer, Create

from keyboards import kb
from rich import print
import time
from data.database import WorkDB
from keyboards.kb import my_requests
from rich.console import Console

db = WorkDB("./data/main.db")

router = Router()

console = Console()


@router.message(CommandStart())
async def start(message : Message):
    if not message.from_user.username: 
        await message.answer(f"Простите дорогой пиользователь, для того чтобы использовать нашего бота вам нужно в настройках телеграма указать <i>имя пользователя</i>", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(f"Здравствуй <b>{message.from_user.full_name}</b>\nЕсли что-то не понятно, или нужна помощь, то пишите - <b>/help</b>", reply_markup=kb.main)
        db.setUser(message.from_user.id, message.from_user.full_name, "@" + message.from_user.username)    



@router.message(F.text.lower() == "/help")
async def help(message: Message):
    await message.answer("<b>1</b>. Чтобы перейти в личный кабинет - нажмите на кнопку Личный Кабинет в меню.\n \n<b>2</b>. Дабы найти запросы - нажмите на кнопку Поиск в меню. А также выберите тип поиска и введите искомый текст. Бот найдет все запросы по заданному тексту. Вы можете просмотреть запросы и увидеть их ответы, которые вы можете оценивать Лайком или Дизлайком.\n \n<b>3</b>. Внутри Личного кабинета есть возможности:\n    • Создать запрос с помощью одноименной кнопки.\n    • При нажатии на кнопку Мои Запросы можно увидеть все созданные вами запросы. Здесь можно отредактировать, просмотреть ответы и удалить запрос. Если на ваш запрос ответили вам придёт уведомление.\n    • В разделе Мои Ответы можно просмотреть ответы, данные вами на другие запросы. Их также можно отредактировать или удалить.\n \n<b>4</b>. Таблица Рейтинга - здесь отмечены последние пять пользователей, у которых наибольшая сумма лайков на их ответах.\n", reply_markup=kb.main)

    

@router.message(F.text.lower() == "на главный экран")
async def cmd_refund(message: Message):
    await message.reply(f"выберите один пункт",
                        reply_markup=kb.main)


@router.message(F.text.lower() == "личный кабинет")
async def cmd_refund(message: Message):   
    db.setUser(message.from_user.id, message.from_user.full_name, "@"+message.from_user.username)
    res = db.my_acc(message.from_user.id)
    await message.reply(f"<b>@{message.from_user.username}</b>\n \nВы дали ответ на {res[1]} запросов\nВы оставили {res[2]} запросов\nКол-во лайков: {res[0]}",
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


@router.message(F.text.lower() == "таблица рейтинга📈")
async def cmd_refund(message: Message):
    res = db.rating() 
    i = 1
    
    for user in res:
        if i == 1:
            await message.answer(f"🥇Лидер🥇\nПользователь: <b>{user[0]}</b>\nКол-во лайков: <b>{user[1]}</b>")
        elif i == 2:
            await message.answer(f"🥈Второе место\nПользователь: <b>{user[0]}</b>\nКол-во лайков: <b>{user[1]}</b>")
        elif i == 3:
            await message.answer(f"🥉Третье место\nПользователь: <b>{user[0]}</b>\nКол-во лайков: <b>{user[1]}</b>")
        else:
            await message.answer(f"Пользователь: <b>{user[0]}</b>\nКол-во лайков: <b>{user[1]}</b>")
        
        i+=1

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
    await message.answer("Осталось немного.\nУкажи теги для своего запроса\n \nПример: <code>Программирование, Языки, Проблема</code>", reply_markup=ReplyKeyboardRemove())


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
        reply_markup=kb.office)
    except Exception:
        console.print_exception(show_locals=True)

