
from aiogram.fsm.state import State, StatesGroup

class FSMComment(StatesGroup):
    user_id = State()
    comment = State()