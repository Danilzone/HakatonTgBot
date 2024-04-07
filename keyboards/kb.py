# Клавиатура


from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardRemove)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Личный кабинет")],
    [KeyboardButton(text="Запросы"), KeyboardButton(text="Рейтинговая таблица")]
],
                            resize_keyboard=True,
                            input_field_placeholder="Выберите пунтк меню.")


office = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Зарегистрироваться"), KeyboardButton(text="На главный экран")],
    [KeyboardButton(text="Мои ответы"), KeyboardButton(text="Мои запросы")]
],
                            resize_keyboard=True,
                            input_field_placeholder="Выберите пунтк меню.")


requests = ReplyKeyboardMarkup(keyboard=[
    [
        [
            KeyboardButton(text="Создать запрос"), 
        ], KeyboardButton(text="На главный экран")
    ],
    
],
                            resize_keyboard=True,
                            input_field_placeholder="Выберите пунтк меню.")


answer = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Ответить на запрос"), KeyboardButton(text="На главный экран")]
],
                            resize_keyboard=True,
                            input_field_placeholder="Выберите пунтк меню.")


def profile(text: str | list):
    builder = ReplyKeyboardBuilder()

    if isinstance(text, str):
        text = [text]

    [builder.button(text=txt) for txt in text]
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


rmk = ReplyKeyboardRemove()