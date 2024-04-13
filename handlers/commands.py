
import ast
from aiogram  import Router, F, types
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command, CommandObject, CommandStart

from aiogram.fsm.context import FSMContext
from utils.states import GetReqEdit
from utils.states import Form, Search,SearchByTags, SetAnswer, EditMyAnswer, Create
from bot import bot
from keyboards import kb
from rich import print
from data.database import WorkDB

from keyboards.kb import my_requests
from rich.console import Console

db = WorkDB("./data/main.db")

router = Router()

console = Console()



@router.message(F.text.lower() == "поиск🔎")
async def cmd_refund(message: Message):
    
    await message.reply(f"выберите один пункт",
                        reply_markup=kb.search)


@router.message(F.text.lower() == "поиск по тегам")
async def cmd_refund(message: Message, state: FSMContext):
    await state.set_state(SearchByTags.text)
    await message.reply(f"Введите теги", reply_markup=ReplyKeyboardRemove())


@router.message(SearchByTags.text)
async def find_text(message: Message, state: FSMContext):
        await state.update_data(text=message.text)
        data = await state.get_data()
        await state.clear()
        text = data.get("text").replace("'", " ").replace('"', ' ').lower()  
        await message.answer(f"Производится поиск по тегам")
        res_db = db.searchRequestTags(text)
        result = []
        i = 0
        for request in res_db: 
            result += [[request[0], request[1], request[2], request[3], request[4]]]
            i +=1
        
        if i == 0:
            await message.answer("Простите, запросов не найдено", reply_markup=kb.main)
        else: 
            await message.answer(f"Результат поиска по тегу(ам): <code>{text}</code> ", reply_markup=kb.list_requests(result))


@router.message(F.text.lower() == "поиск по словам")
async def cmd_refund(message: Message, state: FSMContext):
    await state.set_state(Search.text)
    await message.reply(f"Введите слова для поиска запросов", reply_markup=ReplyKeyboardRemove())


@router.message(Search.text)
async def find_text(message: Message, state: FSMContext):
        await state.update_data(text=message.text)
        data = await state.get_data()
        text = data.get("text").replace("'", " ").replace('"', ' ').lower()
        await state.clear()
        await message.answer(f"Производится поиск: <i>{text}</i>")
        res_db = db.searchRequestText(text)
        result = []
        i = 0
        for request in res_db: 
            result += [[request[0], request[1], request[2], request[3], request[4]]]
            i +=1
        if i == 0:
            await message.answer("Простите, запросов не найдено", reply_markup=kb.main)
        else: 
            await message.answer("Результат поиска: ", reply_markup=kb.list_requests(result))


@router.callback_query(F.data[:4] == "REQ ")
async def my_requests_callback(callback: CallbackQuery):
    await callback.answer(" ")
    request = db.getRequest(callback.from_user.id, callback.data[4:]) # Если в БД есть такой запрос , то в request есть данные  
    if request == None:                                               # ИНАЧЕ он равен None - это значит что в БД нет такого запроса и он выводит сообщение о том что не найдено запроса
        await callback.message.answer("Простите, но такого запросо не найденно :( ", reply_markup=kb.main) # Можем отсюда это убрать, и бот будет молчать
    else:
        await callback.message.answer(f"💠тема: <u>{request[0]}</u>\n• {request[1]}\n \n<code>{request[2]}</code>", reply_markup=kb.interact_request([callback.data[4:], callback.from_user.id]))

      
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
    await state.clear()
    request_title = data.get("title")
    request_ID = data.get("id")
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
    await state.clear()
    request_text = data.get("text")
    request_ID = data.get("id")
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
    await state.clear()
    request_tags = data.get("tags")
    request_ID = data.get("id")
    db.editRequestTags(f"{message.from_user.id}", f"{request_ID}", f"{request_tags}")
    await message.answer("Тэги успешно обновлены")


@router.callback_query(F.data[:5] == "FIND ")
async def other_request_watch(callback: CallbackQuery):    
    data =  ast.literal_eval(callback.data[5:])
    res = db.getRequestById(data)

    try:
        await callback.message.edit_text(f"❓ <u>Запрос от</u> {res[3]}: \n💠<u>тема</u>: {res[4]}\n• {res[5]}\n \n<code>{res[6]}</code>", reply_markup=kb.set_answer(res))
    except Exception:
        console.print_exception(show_locals=True)


@router.callback_query(F.data[:9] == "S_ANSWER ")
async def other_request_set(callback: CallbackQuery, state: FSMContext):    
    data = ast.literal_eval(callback.data[9:])
    await callback.answer(" ")
    await state.set_state(SetAnswer.text)
    await state.update_data(request_id=data)
    await callback.message.reply(f"Пишите ответ")


@router.message(SetAnswer.text)
async def other_request_set(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await state.clear()
    text = data.get("text")
    id = data.get("request_id")
    dogname = "@"+message.from_user.username
    res = db.setAnswer(id, message.from_user.id, "@"+message.from_user.username, text)
    await message.reply("Ваш ответ успешно добавлен", reply_markup=kb.main)

    user_req = db.getRequestById(id)[1]
    if message.from_user.id != user_req:
        title = db.getRequestById(id)[4]
        await bot.send_message(chat_id=res, text=f"Пришел ответ на ваш запрос: <b>{title}</b>\nОт пользователя: <b>{dogname}</b>", reply_markup=kb.check(id))
    else:
        print("ответил на свой же запрос")
    # 
    # 


@router.callback_query(F.data[:9] == "W_ANSWER ")
async def other_request_set(callback: CallbackQuery):    
    data = ast.literal_eval(callback.data[9:])
    await callback.answer(" ")
    res_db = db.getAnswers(data)
    if not res_db:
        await callback.message.answer("К сожалению на этот вопрос нету ответа\nХотите первым на него ответить?", reply_markup=kb.main)
    else:
        for answer in res_db:
            await callback.message.answer(f"❕ <u>ответь от</u>:{answer[3]} \n• {answer[4]}\n \nОценка: <b>{answer[5]}</b>", reply_markup=kb.like_answer(answer[0]))


@router.callback_query(F.data[:7] == "W_A_MR ")
async def other_request_set(callback: CallbackQuery):    
    data = ast.literal_eval(callback.data[7:])
    await callback.answer(" ")
    res_db = db.getAnswers(data[0])
    if not res_db:
        await callback.message.answer("К сожалению на этот вопрос нету ответа", reply_markup=kb.main)
    else:
        for answer in res_db:
            await callback.message.answer(f"❕ <u>ответь от</u>:{answer[3]} \n• {answer[4]}\n \nОценка: <b>{answer[5]}</b>", reply_markup=kb.main)

      
@router.callback_query(F.data[:6] == "DEL_A ")
async def delete_my_requests_callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer(" ")
    db.deleteAnswer(callback.data[6:])
    await callback.message.answer("Вы удалили ответ")


@router.callback_query(F.data == "Back")
async def cmd_refund_clbk(callback: CallbackQuery):
    await callback.answer(" ")
    await callback.message.delete()
    await callback.message.answer(f"выберите один пункт", reply_markup=kb.main)


@router.callback_query(F.data[:7] == "EDIT_A ")
async def edit_my_requests_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(EditMyAnswer.text)
    await state.update_data(answer_id=callback.data[7:])
    await callback.answer(" ")
    await callback.message.reply(f"Вводите новый текст ответа")


@router.message(EditMyAnswer.text)
async def find_text(message: Message, state: FSMContext):
        await state.update_data(text=message.text)
        data = await state.get_data()
        await state.clear()
        text = data.get("text")
        id = data.get("answer_id")
        db.editAnswer(id, message.from_user.id, text)
        await message.reply("Успешно обновлено!")


@router.callback_query(F.data[:5] == "LIKE ")
async def edit_my_requests_callback(callback: CallbackQuery):
    await callback.answer(" ")
    print(callback.data[5:])
    res = db.like(callback.data[5:], callback.message.chat.id)
        
    if res == True:
        await callback.message.reply(f"Лайк поставлен",  reply_markup=kb.main)
    elif res == "No Find":
        await callback.message.reply(f"Этот коментарий уже удален", reply_markup=kb.main)
    else:
        await callback.message.reply(f"Вы уже оценили этот коментарий", reply_markup=kb.main)


@router.callback_query(F.data[:8] == "DISLIKE ")
async def edit_my_requests_callback(callback: CallbackQuery):
    await callback.answer(" ")
    print(callback.data[8:])
    res = db.dislike(callback.data[8:], callback.message.chat.id)
        
    if res == True:
        await callback.message.reply(f"Дизлайк поставлен",  reply_markup=kb.main)
    elif res == "No Find":
        await callback.message.reply(f"Этот коментарий уже удален", reply_markup=kb.main)
    else:
        await callback.message.reply(f"Вы уже оценили этот коментарий", reply_markup=kb.main)


@router.callback_query(F.data[:6] == "CHECK ")
async def check(callback: CallbackQuery):
    await callback.answer(" ")
    res_db = db.getAnswers(callback.data[6:])
    if not res_db:
        await callback.message.answer("К сожалению на этот вопрос нету ответа\nХотите первым на него ответить?", reply_markup=kb.main)
    else:
        for answer in res_db:
            await callback.message.answer(f"❕ <u>ответь от</u>:{answer[3]} \n• {answer[4]}\n \nОценка: <b>{answer[5]}</b>", reply_markup=kb.like_answer(answer[0]))



"""
Работа с БД

db.getRequest(юзер_id, id_запроса)  -> получить статью пользователя 
db.getRequests(юзер_id)             -> получить все статьи пользователя 

db.setRequest(юзер_id, имя_юзера, собачка_юзера, заголовок_запроса, текст_запроса)            -> добавить статью 

"""