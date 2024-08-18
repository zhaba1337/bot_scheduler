import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram import F

from datetime import datetime 
import calendar 

import emoji 

from sup_function import *
from CallBacks import *
from db import *
from handlers import admin, setWeekend

logging.basicConfig(level=logging.INFO)




bot = Bot(token="5135804286:AAEZa-5XFLKT35uc8kOMPoN6kk5hQuHPFBA")

dp = Dispatcher()



@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    con, cur = create_connect()
    if (len(cur.execute('select id from Clients WHERE telegram_id = ?', (message.from_user.id,)).fetchall()) == 0):
        cur.execute("INSERT INTO Clients (telegram_id, first_name, second_name) VALUES (?, ?, ?)", (message.from_user.id, message.from_user.username, message.from_user.last_name))
        close_connect(con)
    await message.answer("write /calendar")

# SELECT date_with_timezone FROM Datetime_slots
# group by date_with_timezone
# HAVING count(*) = 4

@dp.message(Command('calendar'))
async def get_calendar(message: types.Message):
    
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    obj = calendar.Calendar(0).monthdays2calendar(current_year, current_month)
    
    
    builder = InlineKeyboardBuilder()
    
    cb_next = My_cb(name = 'next', message_id=message.message_id, chat_id=message.chat.id, current_year = current_year, current_month = current_month).pack()
    #cb_prev = My_cb(name = 'prev', message_id=message.message_id, chat_id=message.chat.id, current_year = current_year, current_month = current_month).pack()

    builder.row(
        types.InlineKeyboardButton(
                text= '<',
                callback_data='qwe'),
        
        types.InlineKeyboardButton(
                text= f"{calendar.month_name[current_month]} {current_year}",
                callback_data="qwe"),
        
        types.InlineKeyboardButton(
                text= '>',
                callback_data=cb_next)
    )
    
    builder.row(*[types.InlineKeyboardButton(text= i, callback_data="qwe") for i in ('Пн', "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")])
    builder = create_calendar(obj, builder, current_year, current_month, My_cb_date)
        
    await message.answer(
        "Calendar",
        reply_markup=builder.as_markup()
    )            
            

@dp.callback_query(My_cb_date.filter(F.name == 'date'))
async def select_time_edit_message(callback: types.CallbackQuery, callback_data: My_cb_date):
    con, cur = create_connect()
    
    busy_time_slots = cur.execute('SELECT time_slot_id from Datetime_slots WHERE date_with_timezone = ?', (callback_data.date,)).fetchall()
    
    close_connect(con)
    
    builder = InlineKeyboardBuilder()
    lst = ['09:00-12:00', '12:00-15:00', '15:00-18:00', '18:00-21:00']
    
    for time_slot in busy_time_slots:
        lst[time_slot[0]-1] += ' ' + emoji.emojize(':cross_mark:')
    for i in range(len(lst)):
        if(emoji.emoji_count(lst[i])):
            for_callback = My_cb_date_and_time(name='QWE', date=callback_data.date, time=-1).pack()
        else:
            for_callback = My_cb_date_and_time(name='finish', date=callback_data.date, time=i).pack()
        builder.row(types.InlineKeyboardButton(text=f"{lst[i]}", callback_data=for_callback))
    
    current_date = prev_month(datetime.strptime(callback_data.date, '%Y-%m-%d'))   
    back_btn_callback = My_cb(name = 'next', message_id=callback.message.message_id , chat_id=callback.message.chat.id, current_year = current_date.year, current_month = current_date.month).pack()
    
    builder.row(types.InlineKeyboardButton(text='back', callback_data = back_btn_callback))
    await callback.message.edit_text(text=f"{callback_data.date}\n{busy_time_slots}", reply_markup=builder.as_markup())
    await callback.answer()


@dp.callback_query(My_cb_date_and_time.filter(F.name == 'finish'))
async def select_time_edit_message(callback: types.CallbackQuery, callback_data: My_cb_date_and_time):
    lst =['09:00-12:00', '12:00-15:00', '15:00-18:00', '18:00-21:00']
    await callback.message.edit_text(text=f"дата: {callback_data.date} \nвремя: {lst[callback_data.time]} {emoji.emojize(':brain:')}")
    con, cur = create_connect()
    con.execute('INSERT INTO Datetime_slots (date_with_timezone, time_slot_id) VALUES (?, ?)', (callback_data.date, callback_data.time+1))
    con.commit()
    con.execute(
        """INSERT INTO Records (client_id, datetime_slot_id, is_weekend) 
            VALUES (
                (SELECT id from Clients where telegram_id = ?),
                LAST_INSERT_ROWID(),
                0
            )
        """, 
        (callback.from_user.id,)
    )
    close_connect(con)
    await callback.answer()
    





@dp.callback_query(My_cb.filter(F.name == 'prev'))
async def prev_month_edit_message(callback: types.CallbackQuery, callback_data: My_cb):
    
    current_date = prev_month(datetime(callback_data.current_year, callback_data.current_month, 1, 0, 0))
    today_date = datetime.now()
    current_year, current_month = current_date.year, current_date.month
    
    obj = calendar.Calendar(0).monthdays2calendar(current_year, current_month)
    builder = InlineKeyboardBuilder()
    cb_next = My_cb(name = 'next', message_id=callback_data.message_id, chat_id=callback_data.chat_id, current_year = current_year, current_month = current_month).pack()
    
    if(today_date.month == current_month and today_date.year == current_year):
        cb_prev = "qwe"
        
    else:    
        cb_prev = My_cb(name = 'prev', message_id=callback_data.message_id, chat_id=callback_data.chat_id, current_year = current_year, current_month = current_month).pack()


    builder.row(
        types.InlineKeyboardButton(
                text= '<',
                callback_data=cb_prev),
        
        types.InlineKeyboardButton(
                text= f"{calendar.month_name[current_month]} {current_year}",
                callback_data="qwe"),
        
        types.InlineKeyboardButton(
                text= '>',
                callback_data=cb_next)
    )
    
    builder.row(*[types.InlineKeyboardButton(text= i, callback_data="qwe") for i in ('Пн', "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")])
    builder = create_calendar(obj, builder, current_year, current_month, My_cb_date)
        
    await callback.message.edit_text(text=callback_data.name, reply_markup=builder.as_markup())
    await callback.answer()    
    

    
@dp.callback_query(My_cb.filter(F.name == 'next'))
async def next_month_edit_message(callback: types.CallbackQuery, callback_data: My_cb):
    
    current_date = next_month(datetime(callback_data.current_year, callback_data.current_month, 1, 0, 0))
    
    current_year, current_month = current_date.year, current_date.month
    
    obj = calendar.Calendar(0).monthdays2calendar(current_year, current_month)
    
    builder = InlineKeyboardBuilder()
    cb_next = My_cb(name = 'next', message_id=callback_data.message_id, chat_id=callback_data.chat_id, current_year = current_year, current_month = current_month).pack()
    cb_prev = My_cb(name = 'prev', message_id=callback_data.message_id, chat_id=callback_data.chat_id, current_year = current_year, current_month = current_month).pack()

    builder.row(
        types.InlineKeyboardButton(
                text= '<',
                callback_data=cb_prev),
        
        types.InlineKeyboardButton(
                text= f"{calendar.month_name[current_month]} {current_year}",
                callback_data="qwe"),
        
        types.InlineKeyboardButton(
                text= '>',
                callback_data=cb_next)
    )
    
    builder.row(*[types.InlineKeyboardButton(text= i, callback_data="qwe") for i in ('Пн', "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")])
    builder = create_calendar(obj, builder, current_year, current_month, My_cb_date)
        
    await callback.message.edit_text(text=callback_data.name, reply_markup=builder.as_markup())
    await callback.answer()    
    
    
async def main():
    dp.include_routers(admin.router, setWeekend.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())