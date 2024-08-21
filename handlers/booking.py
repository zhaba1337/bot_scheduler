from aiogram import Router, F
from aiogram.filters import Command
from aiogram import types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

import emoji, calendar
from datetime import datetime

from db import create_connect, close_connect
from sup_function import create_calendar, prev_month, next_month
from CallBacks import CB_booking
from kbs.ikb_calendar import kb_builder_calendar, ikb_new, ikb_builder_owner_accept_reject, ikb_builder_owner_comment, ikb_builder_time_slots
router = Router()

@router.message(Command('booking'))
async def start_booking(message: types.Message):

    year = datetime.now().year
    month = datetime.now().month

    CB_next_month = CB_booking(name = 'next_month', date=f"{year}-{month}").pack()
    builder = kb_builder_calendar(year, month, 'empty', CB_next_month)
    
    await message.answer('Пожалуйста выберите число:', reply_markup=builder.as_markup())
    
    
@router.callback_query(CB_booking.filter(F.name == 'choice_time_slot'))
async def select_time_edit_message(callback: types.CallbackQuery, callback_data: CB_booking):

    builder = ikb_builder_time_slots(date=callback_data.date)

    await callback.message.edit_text(text=f"Выберите время которое вас интересует:", reply_markup=builder.as_markup())

    await callback.answer()
    
@router.callback_query(CB_booking.filter(F.name == 'accept_data'))
async def select_time_edit_message(callback: types.CallbackQuery, callback_data: CB_booking):
    
    cb_accept = CB_booking(name='send_book_to_owner', date=callback_data.date, time_slot=callback_data.time_slot, client_username=callback.message.from_user.username).pack()
    cb_back = CB_booking(name='choice_time_slot', date=callback_data.date).pack()
    builder = InlineKeyboardBuilder()
    builder.row(ikb_new('Принять', cb_accept), ikb_new('Назад', cb_back))
    
    await callback.message.answer(f"{type(callback_data)}, {type(cb_accept)}")
    await callback.message.answer(callback.message.from_user.username)