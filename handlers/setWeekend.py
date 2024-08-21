from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

import calendar

from db import create_connect, close_connect
from CallBacks import Admin_cb, Adm_change_year_cb, My_cb_date
from sup_function import create_calendar


router = Router()


@router.message(Command("setweekend"))  
async def get_busy_days_start(message: Message):

    current_month = datetime.now().month
    current_year = datetime.now().year
    
    obj = calendar.Calendar(0).monthdays2calendar(current_year, current_month)
    
    
    builder = InlineKeyboardBuilder()
    

    builder.row(
        types.InlineKeyboardButton(
                text= '<',
                callback_data='qwe'),
        
        types.InlineKeyboardButton(
                text= f"{calendar.month_name[current_month]} {current_year}",
                callback_data="qwe"),
        
        types.InlineKeyboardButton(
                text= '>',
                callback_data='next')
    )
    
    builder.row(*[types.InlineKeyboardButton(text= i, callback_data="qwe") for i in ('Пн', "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")])
    builder = create_calendar(obj, builder, current_year, current_month, My_cb_date, 'set_weekend')
        
    await message.answer(
        "Calendar",
        reply_markup=builder.as_markup()
    )            
    

@router.callback_query(My_cb_date.filter(F.name == 'set_weekend'))
async def set_weekend(callback: types.CallbackQuery, callback_data: My_cb_date):
    
    con, cur = create_connect()

    con.executemany("INSERT INTO Records (datetime_slot_id, is_weekend) VALUES (?, ?)", 
                [(i[0], 1) for i in cur.execute('select id from Datetime_slots order by id desc limit 4').fetchall()])
    
    close_connect(con)
    
    await callback.answer(callback_data.date)