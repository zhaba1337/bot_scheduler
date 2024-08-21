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
    client_username: str
    
    
class CB_booking(CallbackData, prefix='booking client'):
    name: str = 'empty'
    date: str = '0000-00-00'
    time_slot: int = '0'
    client_username: str = 'empty'



class Admin_cb(CallbackData, prefix='admin'):
    name: str
    month: str
    returned_format: int
    





class Adm_change_year_cb(CallbackData, prefix='adm change year'):
    name: str
    year: int
    
class Owner_selection(CallbackData, prefix='accept, reject'):
    name: str
    client_id: int
    date: str
    time: int