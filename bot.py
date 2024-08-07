import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import random 
from aiogram import F
from aiogram.filters.callback_data import CallbackData

from datetime import datetime 



logging.basicConfig(level=logging.INFO)


import calendar 

bot = Bot(token="5135804286:AAEZa-5XFLKT35uc8kOMPoN6kk5hQuHPFBA")

dp = Dispatcher()

class My_cb(CallbackData, prefix='my'):
    name: str
    message_id: int
    chat_id: int
    current_year: int
    current_month: int

class My_cb_date(CallbackData, prefix='date'):
    name: str
    date: str

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")



@dp.message(Command('calendar'))
async def get_calendar(message: types.Message):
    
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    obj = calendar.Calendar(0).monthdays2calendar(current_year, current_month)
    
    
    builder = InlineKeyboardBuilder()
    
    cb_next = My_cb(name = 'next', message_id=message.message_id, chat_id=message.chat.id, current_year = current_year, current_month = current_month).pack()
    cb_prev = My_cb(name = 'prev', message_id=message.message_id, chat_id=message.chat.id, current_year = current_year, current_month = current_month).pack()

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
        
        
    await message.answer(
        "Calendar",
        reply_markup=builder.as_markup()
    )            
            

@dp.callback_query(My_cb_date.filter(F.name == 'date'))
async def prev_month_edit_message(callback: types.CallbackQuery, callback_data: My_cb_date):
    await callback.message.answer(callback_data.date)
    await callback.answer()



@dp.callback_query(My_cb.filter(F.name == 'prev'))
async def prev_month_edit_message(callback: types.CallbackQuery, callback_data: My_cb):
    
    current_year, current_month = callback_data.current_year - (callback_data.current_month)//12, (callback_data.current_month)%12-1
    
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
    

    
@dp.callback_query(My_cb.filter(F.name == 'next'))
async def next_month_edit_message(callback: types.CallbackQuery, callback_data: My_cb):
    
    current_year, current_month = callback_data.current_year + (callback_data.current_month)//12, (callback_data.current_month)%12+1
    
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