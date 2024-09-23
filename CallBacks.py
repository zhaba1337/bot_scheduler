from aiogram.filters.callback_data import CallbackData
from db import DB_connector
from typing import List, Any

import json


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

    def for_owner(self) -> str:
        return f"@{self.client_username}, дата: {self.date}, временной интервал: {DB_connector().get_time_slots()[self.time_slot-1]}"

    def for_client(self) -> str:
        return f"\nДата: {self.date}, временной интервал: {DB_connector().get_time_slots()[self.time_slot-1]}"
    
    def for_accept_bid(self) -> List[Any]:
        return [self.client_username, self.date, self.time_slot]
    
    def get_json_cash(self) -> str:
        returable_json = {
            'state' : self.name, 
            'date' : self.date, 
            'time_slot' : self.time_slot
        }
        return json.dumps(returable_json)
    
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