from aiogram.filters.callback_data import CallbackData


class My_cb(CallbackData, prefix='my'):
    name: str
    message_id: int
    chat_id: int
    current_year: int
    current_month: int


class My_cb_date(CallbackData, prefix='date'):
    name: str
    date: str

    
    
class My_cb_date_and_time(CallbackData, prefix='date_and_time'):
    name: str
    date: str
    time: int