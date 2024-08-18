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

from CallBacks import Admin_cb, Adm_change_year_cb

router = Router()



def builder_all_months(builder, year):
    months = calendar.month_name
    for month_index in range(len(months)):
        adm_cb = Admin_cb(name='get_month', month=f"{year}-{str(month_index).zfill(2)}-01", returned_format=0).pack()
        builder.row(types.InlineKeyboardButton(text = months[month_index].capitalize(), callback_data=adm_cb))

    return builder



@router.message(Command("busydays"))  
async def get_busy_days_start(message: Message):
    
    builder = InlineKeyboardBuilder()

    current_year = datetime.now().year
    
    builder.row(
        types.InlineKeyboardButton(text = '<', callback_data=Adm_change_year_cb(name='prev', year=current_year).pack()),
        types.InlineKeyboardButton(text = str(current_year), callback_data='qwe'),
        types.InlineKeyboardButton(text = '>', callback_data=Adm_change_year_cb(name='next', year=current_year).pack())
    )
     
    builder = builder_all_months(builder, current_year)

    await message.answer('choice month  ', reply_markup=builder.as_markup())
    
    
@router.callback_query(Admin_cb.filter(F.name == 'get_month'))
async def get_busy_days_get_month(callback: types.CallbackQuery, callback_data: Admin_cb):
    builder = InlineKeyboardBuilder()
    builder.add(
        #types.InlineKeyboardButton(text = 'html', callback_data=Admin_cb(name='finish', month=callback_data.month, returned_format=1).pack()),
        types.InlineKeyboardButton(text = 'table', callback_data=Admin_cb(name='finish', month=callback_data.month, returned_format=2).pack()),
        #types.InlineKeyboardButton(text = 'future', callback_data=Admin_cb(name='finish', month=callback_data.month, returned_format=3).pack())
        )
    
    await callback.message.edit_text(text='choice returned type busy days', reply_markup=builder.as_markup())
    await callback.answer()
    
    
@router.callback_query(Admin_cb.filter(F.name == 'finish'))
async def get_busy_days_finish(callback: types.CallbackQuery, callback_data: Admin_cb):
    con, cur = create_connect()
    time_slots = ['9:00-12:00', '12:00-15:00', "15:00-18:00", "18:00-21:00"]
    busy_days_in_current_month = cur.execute("""
                SELECT Clients.first_name, Datetime_slots.date_with_timezone, Datetime_slots.time_slot_id FROM Records
                INNER JOIN Clients ON Records.client_id = Clients.id
                INNER JOIN Datetime_slots ON Datetime_slots.id = datetime_slot_id
                WHERE date_with_timezone BETWEEN ? AND date(?, '+1 month', '-1 days') and NOT(Records.is_weekend)
                """, (callback_data.month, callback_data.month)).fetchall()
    close_connect(con)
    
    
    match callback_data.returned_format:
        case 1:#html
            pass
        
        case 2:#table
            text ='busy days:\n'
            for i in busy_days_in_current_month:
                text += f"client: @{i[0]} date: {i[1]} time: {time_slots[i[2]-1]}\n"
               
        
        case 3:#future
            pass
        
    await callback.message.edit_text(text)
    await callback.answer()
    
@router.callback_query(Adm_change_year_cb.filter(F.name == 'next'))
async def get_busy_days_finish(callback: types.CallbackQuery, callback_data: Adm_change_year_cb):
    builder = InlineKeyboardBuilder()

    current_year = callback_data.year+1
    
    builder.row(
        types.InlineKeyboardButton(text = '<', callback_data=Adm_change_year_cb(name='prev', year=current_year).pack()),
        types.InlineKeyboardButton(text = str(current_year), callback_data='qwe'),
        types.InlineKeyboardButton(text = '>', callback_data=Adm_change_year_cb(name='next', year=current_year).pack())
    )
     
    builder = builder_all_months(builder, current_year)

    await callback.message.edit_text('choice month  ', reply_markup=builder.as_markup())

@router.callback_query(Adm_change_year_cb.filter(F.name == 'prev'))
async def get_busy_days_finish(callback: types.CallbackQuery, callback_data: Adm_change_year_cb):
    builder = InlineKeyboardBuilder()

    current_year = callback_data.year-1
    
    builder.row(
        types.InlineKeyboardButton(text = '<', callback_data=Adm_change_year_cb(name='prev', year=current_year).pack()),
        types.InlineKeyboardButton(text = str(current_year), callback_data='qwe'),
        types.InlineKeyboardButton(text = '>', callback_data=Adm_change_year_cb(name='next', year=current_year).pack())
    )
     
    builder = builder_all_months(builder, current_year)
    await callback.message.edit_text('choice month  ', reply_markup=builder.as_markup())