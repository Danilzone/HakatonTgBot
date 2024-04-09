
import ast
from aiogram  import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject, CommandStart

from aiogram.fsm.context import FSMContext
from utils.states import GetReqEdit
from utils.states import Form, Search

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



@router.message(F.text.lower() == "поиск🔎")
async def cmd_refund(message: Message):
    await message.reply(f"выберите один пункт",
                        reply_markup=kb.search)


@router.message(F.text.lower() == "поиск по словам")
async def cmd_refund(message: Message, state: FSMContext):
    await state.set_state(Search.text)
    await message.reply(f"Введите слова для поиска запросов")


@router.message(Search.text)
async def find_text(message: Message, state: FSMContext):

        await state.update_data(text=message.text)
        data = await state.get_data()
        text = data.get("text")
        await message.reply(f"Производится поиск {text}")
        
# 

@router.message(F.text.lower() == "рейтинговая таблица")
async def cmd_refund(message: Message):
    await message.reply(f"выберите один пункт",
                        reply_markup=kb.answer)



# Тут мы получаем инфу с инлайн кнопок и выводим из бд нужный 'запрос'

@router.callback_query(F.data[:4] == "REQ ")
async def my_requests_callback(callback: CallbackQuery):
    await callback.answer(" ")
    request = db.getRequest(callback.from_user.id, callback.data[4:]) # Если в БД есть такой запрос , то в request есть данные  
    if request == None:                                               # ИНАЧЕ он равен None - это значит что в БД нет такого запроса и он выводит сообщение о том что не найдено запроса
        print("Ой")
        await callback.message.answer("Простите, но такого запросо не найденно :( ") # Можем отсюда это убрать, и бот будет молчать
    else:
        await callback.message.answer(f"💠тема: <u>{request[0]}</u>\n• {request[1]}", reply_markup=kb.interact_request([callback.data[4:], callback.from_user.id]))

      
@router.callback_query(F.data[:4] == "DEL ")
async def delete_my_requests_callback(callback: CallbackQuery):
    await callback.message.delete()
    
    data =  ast.literal_eval(callback.data[4:])
    await callback.answer(" ")
    db.deleteRequest(data[0], callback.from_user.id)
    await callback.message.answer("Вы удалили запрос")


@router.callback_query(F.data[:5] == "EDIT ")
async def edit_my_requests_callback(callback: CallbackQuery):
    data = ast.literal_eval(callback.data[5:])
    await callback.answer(" ")
    print(type(data))
    await callback.message.edit_text(f"Что хотите отредактировать?", reply_markup=kb.edit_request_inline( data ))


@router.callback_query(F.data[:6] == "TITLE ")
async def edit_my_requests_callback(callback: CallbackQuery, state: FSMContext):
    data = ast.literal_eval(callback.data[6:])
    await callback.answer(" ")
    await state.set_state(Form.request_title)
    await state.update_data(id=data)
    await callback.message.edit_text(f"Введите новый заголовог")


@router.message(Form.request_title)
async def new_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    data = await state.get_data()
    print(data)
    await state.clear()
    request_title = data.get("title")
    request_ID = data.get("id")
    print(request_title, request_ID)
    db.editRequestTitle(f"{message.from_user.id}", f"{request_ID}", f"{request_title}")
    await message.answer("Тема успешно обновлена")


@router.callback_query(F.data[:5] == "TEXT ")
async def edit_my_requests_callback(callback: CallbackQuery, state: FSMContext):
    data = ast.literal_eval(callback.data[5:])
    await callback.answer(" ")
    await state.set_state(Form.request_text)
    await state.update_data(id=data)
    await callback.message.edit_text(f"Введите новый текст")


@router.message(Form.request_text)
async def new_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    print(data)
    await state.clear()
    request_text = data.get("text")
    request_ID = data.get("id")
    print(request_text, request_ID)
    db.editRequestText(f"{message.from_user.id}", f"{request_ID}", f"{request_text}")
    await message.answer("Текст успешно обновлен")

    

@router.callback_query(F.data[:5] == "TAGS ")
async def edit_my_requests_callback(callback: CallbackQuery, state: FSMContext):
    data = ast.literal_eval(callback.data[5:])
    await callback.answer(" ")
    await state.set_state(Form.request_tags)
    await state.update_data(id=data)
    await callback.message.edit_text(f"Введите новые теги")


@router.message(Form.request_tags)
async def new_tags(message: Message, state: FSMContext):
    await state.update_data(tags=message.text)
    data = await state.get_data()
    print(data)
    await state.clear()
    request_tags = data.get("tags")
    request_ID = data.get("id")
    print(request_tags, request_ID)
    db.editRequestTags(f"{message.from_user.id}", f"{request_ID}", f"{request_tags}")
    await message.answer("Тэги успешно обновлены")
# 
# 

"""
Работа с БД

db.getRequest(юзер_id, id_запроса)  -> получить статью пользователя 
db.getRequests(юзер_id)             -> получить все статьи пользователя 

db.setRequest(юзер_id, имя_юзера, собачка_юзера, заголовок_запроса, текст_запроса)            -> добавить статью 

"""