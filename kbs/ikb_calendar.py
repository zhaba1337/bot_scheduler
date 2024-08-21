from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from datetime import datetime
import calendar
from db import create_connect, close_connect
from sup_function import create_calendar, prev_month, next_month
from CallBacks import My_cb, My_cb_date, My_cb_date_and_time, Owner_selection, CB_booking

from aiogram.filters.callback_data import CallbackData



def ikb_new(text: str, callback_data: CallbackData | str) -> types.InlineKeyboardButton:
    return types.InlineKeyboardButton(text=text, callback_data=callback_data)
 

def kb_calendar_names_row(prev_cb, next_cb, text):
    return [
        types.InlineKeyboardButton(
                text= '<',
                callback_data=prev_cb
                ),
        types.InlineKeyboardButton(
                text= text,
                callback_data='empty'
                ),
        types.InlineKeyboardButton(
                text= '>',
                callback_data=next_cb
                )
        ]

def kb_builder_calendar(year, month, prev_cb, next_cb) -> InlineKeyboardBuilder:
    
    builder = InlineKeyboardBuilder()
    builder.row(*kb_calendar_names_row(prev_cb=prev_cb, next_cb=next_cb, text=f"{calendar.month_name[month]} {year}"))
    builder.row(*[types.InlineKeyboardButton(text= i, callback_data="empty") for i in ('Пн', "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")])
    obj = calendar.Calendar(0).monthdays2calendar(year, month)
    builder = create_calendar(obj, builder, year, month, CB_booking)

    return builder



 
def ikb_builder_time_slots(date: str) -> InlineKeyboardBuilder:
    con, cur = create_connect()
    free_slots = cur.execute("""
                            SELECT Time_slots.id, Time_slots.start_at, Time_slots.end_at
                            FROM Datetime_slots
                            JOIN Time_slots ON Time_slots.id = time_slot_id
                            WHERE date_with_timezone = ?
                            AND NOT(iif(Datetime_slots.id in (select datetime_slot_id from Records), 1, 0))
                             """
                             , (date,)).fetchall()
    
    close_connect(con)
    builder = InlineKeyboardBuilder()
    for i in free_slots:
        for_callback = CB_booking(name='accept_data', date=date, time_slot=i[0]).pack()
        builder.row(types.InlineKeyboardButton(text=f"{i[1]}:00-{i[2]}:00", callback_data=for_callback))
    
    current_date = prev_month(datetime.strptime(date, '%Y-%m-%d')) 
    back_btn_callback = CB_booking(name = 'next_month', current_year = current_date.year, current_month = current_date.month).pack()
    builder.row(types.InlineKeyboardButton(text='назад', callback_data = back_btn_callback))
    return builder
    
    
    
def ikb_builder_owner_accept_reject(client_id, date, time) -> InlineKeyboardBuilder:
    
    builder = InlineKeyboardBuilder()
    
    cb_accept = Owner_selection(name='accept', client_id=client_id, date=date, time=time)
    cb_reject = Owner_selection(name='reject', client_id=client_id, date='-', time = -1)
    
    builder.row(ikb_new('Принять запись', cb_accept), ikb_new('Отказать', cb_reject))
    
    return builder


def ikb_builder_owner_comment(client_id) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    cb_accept =Owner_selection(name='comment_accept', client_id=client_id, date='qwe', time=-1)
    cb_reject =Owner_selection(name='comment_reject', client_id=client_id, date='qwe', time=-1)
    
    builder.row(ikb_new('Принять запись', cb_accept), ikb_new('Отказать', cb_reject))
    
    return builder