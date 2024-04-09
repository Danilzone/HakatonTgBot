from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    request_title = State()
    request_text = State()
    request_tags = State()
    request_id = State()
    # about = State()
    # photo = State()


class Create(StatesGroup):
    request_title = State()
    request_text = State()
    request_tags = State()
    request_id = State()


class Search(StatesGroup):
    text = State()

class GetReqEdit(StatesGroup):
    request_main = State()


class NewTitle(StatesGroup):
    new_title = State()


class NewText(StatesGroup):
    new_text = State()


class NewTag(StatesGroup):
    new_tag = State()