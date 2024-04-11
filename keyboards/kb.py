# Клавиатура
from rich import print

from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardRemove)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Личный кабинет")],
    [KeyboardButton(text="Поиск🔎"), KeyboardButton(text="Рейтинговая таблица")]
],
                            resize_keyboard=True,
                            input_field_placeholder="Выберите пунтк меню.")


office = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Создать запрос"), KeyboardButton(text="На главный экран")],
    [KeyboardButton(text="Мои ответы"), KeyboardButton(text="Мои запросы")]
],
                            resize_keyboard=True,
                            input_field_placeholder="Выберите пунтк меню.")


# ------------------------------------------------------------
search = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Поиск по словам"), KeyboardButton(text="Поиск по тегам")], 
    [KeyboardButton(text="На главный экран")]
],
                            resize_keyboard=True,)


created_request_inline = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Изменить", callback_data="change"), InlineKeyboardButton(text="Отправить", callback_data="send")],
        [InlineKeyboardButton(text="Отменить", callback_data="delet")],
])
# -----------------------------------------------------------


answer = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Ответить на запрос"), KeyboardButton(text="На главный экран")]
],
                            resize_keyboard=True,
                            input_field_placeholder="Выберите пунтк меню.")


change_request_inline = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Тема", callback_data="change_title"), InlineKeyboardButton(text="Тэг", callback_data="tags")],
        [InlineKeyboardButton(text="Текст", callback_data="text")],
])


def profile(text: str | list):
    builder = ReplyKeyboardBuilder()

    if isinstance(text, str):
        text = [text]

    [builder.button(text=txt[1]) for txt in text]
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def my_requests(text: str | list):
    builder = InlineKeyboardBuilder()
    print(text)
    [builder.row(InlineKeyboardButton(text=f"{txt[1]}", callback_data=f"REQ {txt[0]}")) for txt in text ]
    return builder.adjust(2).as_markup()


def list_requests(text: str | list):
    builder = InlineKeyboardBuilder()
    print(text)
    [builder.row(InlineKeyboardButton(text=f"{txt[3]}", callback_data=f"FIND {txt[0]}")) for txt in text ]
    return builder.adjust(2).as_markup()


def interact_request(text: str | list):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Редактировать", callback_data=f"EDIT {text}"),
        InlineKeyboardButton(text="Удалить", callback_data=f"DEL {text}"),
    )
    return builder.as_markup()


def set_answer(text: str | list):
    builder = InlineKeyboardBuilder()
    print("kb 89 \n \n \n")
    print(text)

    builder.row(
        InlineKeyboardButton(text="Ответить", callback_data=f"S_ANSWER {text[0]}"),
        InlineKeyboardButton(text="Посмотретьт ответы", callback_data=f"W_ANSWER {text[0]}"),
    )
    return builder.adjust(2).as_markup()


def edit_request_inline(text):
    builder = InlineKeyboardBuilder()
    print(text)
    builder.row(
        InlineKeyboardButton(text="Заголовок", callback_data=f"TITLE {text[0]}"),
        InlineKeyboardButton(text="Текст", callback_data=f"TEXT {text[0]}"),
        InlineKeyboardButton(text="Тэги", callback_data=f"TAGS {text[0]}"), width=2
    )
    
    return builder.as_markup()

rmk = ReplyKeyboardRemove()