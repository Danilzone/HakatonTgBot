from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    request_title = State()
    request_text = State()
    request_tags = State()
    # about = State()
    # photo = State()

class GetReqEdit(StatesGroup):
    request_main = State()