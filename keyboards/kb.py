# Клавиатура
from rich import print

from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardRemove)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


creating_a_request = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Изменить", callback_data="change")],
    [InlineKeyboardButton(text="Тэг", callback_data="tag")],
    [InlineKeyboardButton(text="Тема", callback_data="topic")],
    [InlineKeyboardButton(text="Текст", callback_data="text")],
    [InlineKeyboardButton(text="Отправить", callback_data="send")],
    [InlineKeyboardButton(text="Удалить", callback_data="remove")]
])


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Личный кабинет")],
    [KeyboardButton(text="Запросы"), KeyboardButton(text="Рейтинговая таблица")]
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
requests = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Создать запрос"), KeyboardButton(text="Редактировать запрос")], 
    [KeyboardButton(text="На главный экран")]
],
                            resize_keyboard=True,
                            input_field_placeholder="Выберите пунтк меню.")

interact_request = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Редактировать запрос"), KeyboardButton(text="Удалить запрос")],
        [KeyboardButton(text="На главный экран")]
],
                            resize_keyboard=True)

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


def profile(text: str | list):
    builder = ReplyKeyboardBuilder()

    if isinstance(text, str):
        text = [text]

    [builder.button(text=txt[1]) for txt in text]
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def my_requests(text: str |list):
    builder = InlineKeyboardBuilder()

    [builder.row(InlineKeyboardButton(text=f"{txt[1]}", callback_data=f"REQ {txt[0]}")) for txt in text ]
    return builder.as_markup()


rmk = ReplyKeyboardRemove()