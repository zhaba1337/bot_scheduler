import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import random 
from aiogram import F
from aiogram.filters.callback_data import CallbackData

from datetime import datetime 
import calendar 

import emoji 

from sup_function import *
from CallBacks import *


logging.basicConfig(level=logging.INFO)




bot = Bot(token="5135804286:AAEZa-5XFLKT35uc8kOMPoN6kk5hQuHPFBA")

dp = Dispatcher()



@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("write /calendar")



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
    
    for i in obj:
        builder1, data, for_callback = [], '', '-'
        for j in i:
            
            if(j[0]):
                data = str(j[0])
                for_callback = My_cb_date(name='date', date=f"{current_year}.{current_month}.{j[0]}").pack()
            else:
                data = '-'
                for_callback = '-'
                
            builder1.append(types.InlineKeyboardButton(
                text= data,
                callback_data = for_callback)
            )
                
        builder.row(*builder1)
        
        
    await message.answer(
        "Calendar",
        reply_markup=builder.as_markup()
    )            
            

@dp.callback_query(My_cb_date.filter(F.name == 'date'))
async def select_time_edit_message(callback: types.CallbackQuery, callback_data: My_cb_date):

    builder = InlineKeyboardBuilder()
    lst =['09:00-12:00', '12:00-15:00', '15:00-18:00', '18:00-21:00']
    for i in range(len(lst)):
        for_callback = My_cb_date_and_time(name='finish', date=callback_data.date, time=i).pack()
        builder.row(types.InlineKeyboardButton(text=f"{lst[i]} {emoji.emojize(':brain:')}", callback_data=for_callback))
        
    await callback.message.edit_text(text=callback_data.date, reply_markup=builder.as_markup())
    await callback.answer()


@dp.callback_query(My_cb_date_and_time.filter(F.name == 'finish'))
async def select_time_edit_message(callback: types.CallbackQuery, callback_data: My_cb_date_and_time):
    lst =['09:00-12:00', '12:00-15:00', '15:00-18:00', '18:00-21:00']
    await callback.message.edit_text(text=f"дата: {callback_data.date} \nвремя: {lst[callback_data.time]} {emoji.emojize(':brain:')}")
    await callback.answer()

@dp.callback_query(My_cb.filter(F.name == 'prev'))
async def prev_month_edit_message(callback: types.CallbackQuery, callback_data: My_cb):
    
    current_date = prev_month(datetime(callback_data.current_year, callback_data.current_month, 1, 0, 0))
    today_date = datetime.now()
    current_year, current_month = current_date.year, current_date.month
    
    obj = calendar.Calendar(0).monthdays2calendar(current_year, current_month)
    print(today_date)
    print(current_date)
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
    
    for i in obj:
        builder1, data, for_callback = [], '', '-'
        for j in i:
            
            if(j[0]):
                data = str(j[0])
                for_callback = My_cb_date(name='date', date=f"{current_year}.{current_month}.{j[0]}").pack()
            else:
                data = '-'
                for_callback = '-'
                
            builder1.append(types.InlineKeyboardButton(
                text= data,
                callback_data = for_callback)
            )
                
        builder.row(*builder1)
        
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
    
    for i in obj:
        builder1, data, for_callback = [], '', '-'
        for j in i:
            
            if(j[0]):
                data = str(j[0])
                for_callback = My_cb_date(name='date', date=f"{current_year}.{current_month}.{j[0]}").pack()
            else:
                data = '-'
                for_callback = '-'
                
            builder1.append(types.InlineKeyboardButton(
                text= data,
                callback_data = for_callback)
            )
                
        builder.row(*builder1)
        
    await callback.message.edit_text(text=callback_data.name, reply_markup=builder.as_markup())
    await callback.answer()    
    
    
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())