
import ast
from aiogram  import Router, F
from aiogram.types import Message, CallbackQuery
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



@router.message(F.text.lower() == "поиск🔎")
async def cmd_refund(message: Message):
    await message.reply(f"выберите один пункт",
                        reply_markup=kb.search)



@router.message(F.text.lower() == "поиск по тегам")
async def cmd_refund(message: Message, state: FSMContext):
    await state.set_state(SearchByTags.text)
    await message.reply(f"Введите теги")


@router.message(SearchByTags.text)
async def find_text(message: Message, state: FSMContext):
        await state.update_data(text=message.text)
        data = await state.get_data()
        text = data.get("text").replace("'", " ").replace('"', ' ').lower()  

        await message.answer(f"Производится поиск по тегам")
        res_db = db.searchRequestTags(text)
        result = []
        i = 0
        for request in res_db: 
            result += [[request[0], request[1], request[2], request[3], request[4]]]
            i +=1
        
        if i == 0:
            await message.answer("Простите, запросов не найдено")
        else: 
            await message.answer(f"Результат поиска по тегу(ам): <code>{text}</code> ", reply_markup=kb.list_requests(result))


@router.message(F.text.lower() == "поиск по словам")
async def cmd_refund(message: Message, state: FSMContext):
    await state.set_state(Search.text)
    await message.reply(f"Введите слова для поиска запросов")


@router.message(Search.text)
async def find_text(message: Message, state: FSMContext):
        await state.update_data(text=message.text)
        data = await state.get_data()
        text = data.get("text").replace("'", " ").replace('"', ' ').lower()
        await message.answer(f"Производится поиск: <i>{text}</i>")
        res_db = db.searchRequestText(text)
        result = []
        i = 0
        for request in res_db: 
            result += [[request[0], request[1], request[2], request[3], request[4]]]
            i +=1
        if i == 0:
            await message.answer("Простите, запросов не найдено")
        else: 
            await message.answer("Результат поиска: ", reply_markup=kb.list_requests(result))


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
        await callback.message.edit_text(f"❓ <u>Запрос от</u> {res[3]}: \n💠<u>тема</u>: {res[4]}\n• {res[5]}", reply_markup=kb.set_answer(res))
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
    text = data.get("text")
    id = data.get("request_id")
    db.setAnswer(id, message.from_user.id, "@"+message.from_user.username, text)
    await message.reply("Ваш ответ успешно добавлен")


@router.callback_query(F.data[:9] == "W_ANSWER ")
async def other_request_set(callback: CallbackQuery):    
    data = ast.literal_eval(callback.data[9:])
    await callback.answer(" ")
    res_db = db.getAnswers(data)
    if not res_db:
        await callback.message.answer("К сожалению на этот вопрос нету ответа\nХотите первым на него ответить?")
    else:
        for answer in res_db:
            await callback.message.answer(f"❕ <u>ответь от</u>:{answer[3]} \n• {answer[4]}")


@router.callback_query(F.data[:7] == "W_A_MR ")
async def other_request_set(callback: CallbackQuery):    
    data = ast.literal_eval(callback.data[7:])
    await callback.answer(" ")
    res_db = db.getAnswers(data[0])
    if not res_db:
        await callback.message.answer("К сожалению на этот вопрос нету ответа")
    else:
        for answer in res_db:
            await callback.message.answer(f"❕ <u>ответь от</u>:{answer[3]} \n• {answer[4]}")

      
@router.callback_query(F.data[:6] == "DEL_A ")
async def delete_my_requests_callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer(" ")
    db.deleteAnswer(callback.data[6:])
    await callback.message.answer("Вы удалили ответ")


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
        text = data.get("text")
        id = data.get("answer_id")
        db.editAnswer(id, message.from_user.id, text)
        await message.reply("Успешно обновлено!")


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

@router.message()
async def cmd_refund(message: Message):
    await message.reply("Простите, используйте кнопки для навигации")
"""
Работа с БД

db.getRequest(юзер_id, id_запроса)  -> получить статью пользователя 
db.getRequests(юзер_id)             -> получить все статьи пользователя 

db.setRequest(юзер_id, имя_юзера, собачка_юзера, заголовок_запроса, текст_запроса)            -> добавить статью 

"""