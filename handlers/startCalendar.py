from aiogram import Router, F
from aiogram.filters import Command
from aiogram import types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

import emoji, calendar
from datetime import datetime

from db import create_connect, close_connect
from sup_function import create_calendar, prev_month, next_month
from CallBacks import My_cb, My_cb_date, My_cb_date_and_time, Owner_selection

from kbs.ikb_calendar import kb_builder_calendar, ikb_new, ikb_builder_owner_accept_reject, ikb_builder_owner_comment
router = Router()



@router.message(Command('calendar'))
async def get_calendar(message: types.Message):

    current_month = datetime.now().month
    current_year = datetime.now().year
    
    obj = calendar.Calendar(0).monthdays2calendar(current_year, current_month)
    
    cb_next = My_cb(name = 'next', message_id=message.message_id, chat_id=message.chat.id, current_year = current_year, current_month = current_month).pack()
    builder = kb_builder_calendar(current_year, current_month, 'q', cb_next)
    
    await message.answer(
        "Calendar",
        reply_markup=builder.as_markup()
    )            
            
#всё это вообзе под замену 
@router.callback_query(My_cb_date.filter(F.name == 'date'))
async def select_time_edit_message(callback: types.CallbackQuery, callback_data: My_cb_date):
    con, cur = create_connect()

    free_slots = cur.execute("""
                            SELECT Time_slots.id, Time_slots.start_at, Time_slots.end_at
                            FROM Datetime_slots
                            JOIN Time_slots ON Time_slots.id = time_slot_id
                            WHERE date_with_timezone = ?
                            AND NOT(iif(Datetime_slots.id in (select datetime_slot_id from Records), 1, 0))
                             """
                             , (callback_data.date,)).fetchall()
    
    close_connect(con)
    
    builder = InlineKeyboardBuilder()
    
    for i in free_slots:
        for_callback = My_cb_date_and_time(name='finish', date=callback_data.date, time=i[0], client_username='-').pack()
        builder.row(
            types.InlineKeyboardButton(text=f"{i[1]}:00-{i[2]}:00", callback_data=for_callback)
        )
        
    current_date = prev_month(datetime.strptime(callback_data.date, '%Y-%m-%d')) 
    back_btn_callback = My_cb(name = 'next', message_id=callback.message.message_id , chat_id=callback.message.chat.id, current_year = current_date.year, current_month = current_date.month).pack()
    builder.row(types.InlineKeyboardButton(text='back', callback_data = back_btn_callback))
    await callback.message.edit_text(text=f"1111", reply_markup=builder.as_markup())

    await callback.answer()

@router.callback_query(My_cb_date_and_time.filter(F.name == 'finish'))
async def select_time_edit_message(callback: types.CallbackQuery, callback_data: My_cb_date_and_time):
    
    cb_accept = My_cb_date_and_time(name='accept_data', date=callback_data.date, time=callback_data.time, client_username=callback.message.from_user.username).pack()
    cb_back = My_cb_date_and_time(name='date', date=callback_data.date, time=0, client_username='-').pack()
    builder = InlineKeyboardBuilder()
    builder.row(ikb_new('Принять', cb_accept), ikb_new('Назад', cb_back))
    

    await callback.message.edit_text(text=f"дата: {callback_data.date}  \n Все правильно?", reply_markup=builder.as_markup())
    await callback.answer()
    
from bot import Bot
@router.callback_query(My_cb_date_and_time.filter(F.name == 'accept_data'))
async def accept_owner_and_pull_db(callback: types.CallbackQuery, callback_data: My_cb_date_and_time, bot: Bot):
    con, cur = create_connect()
    lst = [f"{i[0]}:00-{i[1]}:00" for i in cur.execute('select start_at, end_at from Time_slots').fetchall()]
    owner = cur.execute('select telegram_id from Owners').fetchone()[0]
    print(callback_data.client_username)
    client_id = cur.execute('select telegram_id from Clients WHERE first_name = ?', (callback_data.client_username,)).fetchone()[0]
    close_connect(con)
    await callback.message.answer(f'принято!\nдата: {callback_data.date}, время: {lst[callback_data.time-1]}. \n дождитесь ответа.')
    await bot.send_message(owner, f"Новая запись от {callback_data.client_username}\nдата: {callback_data.date}, время: {lst[callback_data.time-1]}", 
                           reply_markup=ikb_builder_owner_accept_reject(client_id=client_id, date=callback_data.date, time=callback_data.time).as_markup())


@router.callback_query(Owner_selection.filter(F.name == 'reject'))
async def accept_owner_and_pull_db(callback: types.CallbackQuery, callback_data: Owner_selection, bot: Bot):
    await bot.send_message(callback_data.client_id, 'Ваша заявка отклонена!')
    builder = InlineKeyboardBuilder()
    builder.row(ikb_new('comment', Owner_selection()))
    await callback.message.answer('оставить комментарий?', reply_markup=ikb_builder_owner_comment(callback_data.client_id).as_markup())
    await callback.answer()
    
    
@router.callback_query(Owner_selection.filter(F.name == 'accept'))
async def accept_owner_and_pull_db(callback: types.CallbackQuery, callback_data: Owner_selection, bot: Bot): 

    con, cur = create_connect()
    cur.execute(
        """INSERT INTO Records (client_id, datetime_slot_id, is_weekend) 
            VALUES (
                (SELECT id from Clients where telegram_id = ?),
                (SELECT id FROM Datetime_slots WHERE date_with_timezone = ? AND time_slot_id = ?),
                0)
        """, 
        (callback.from_user.id, callback_data.date, callback_data.time)
    )
    close_connect(con)
    
    await bot.send_message(callback_data.client_id, 'Ваша заявка принята!')
    await callback.message.answer('оставить комментарий?', reply_markup=ikb_builder_owner_comment(callback_data.client_id).as_markup())
    await callback.answer()




@router.callback_query(My_cb.filter(F.name == 'prev'))
async def prev_month_edit_message(callback: types.CallbackQuery, callback_data: My_cb):
    
    current_date = prev_month(datetime(callback_data.current_year, callback_data.current_month, 1, 0, 0))
    today_date = datetime.now()
    current_year, current_month = current_date.year, current_date.month
    cb_next = My_cb(name = 'next', 
                    message_id=callback_data.message_id, 
                    chat_id=callback_data.chat_id, 
                    current_year = current_year, 
                    current_month = current_month
    ).pack()

    if(today_date.month == current_month and today_date.year == current_year):
        cb_prev = "empty"
        
    else:    
        cb_prev = My_cb(name = 'prev',
                        message_id=callback_data.message_id, 
                        chat_id=callback_data.chat_id, 
                        current_year = current_year, 
                        current_month = current_month
        ).pack()

    builder = kb_builder_calendar(current_year, current_month, cb_prev, cb_next)
    await callback.message.edit_text(text=callback_data.name, reply_markup=builder.as_markup())
    await callback.answer("Ваша заявка принята!\n")    
    

    
@router.callback_query(My_cb.filter(F.name == 'next'))
async def next_month_edit_message(callback: types.CallbackQuery, callback_data: My_cb):
    
    current_date = next_month(datetime(callback_data.current_year, callback_data.current_month, 1, 0, 0))    
    current_year, current_month = current_date.year, current_date.month

    cb_prev = My_cb(name = 'prev', 
                    message_id=callback_data.message_id, 
                    chat_id=callback_data.chat_id,
                    current_year = current_year, 
                    current_month = current_month
    ).pack()
    builder = kb_builder_calendar(current_year, current_month, cb_prev, 'empty')
    
    await callback.message.edit_text(text=callback_data.name, reply_markup=builder.as_markup())
    await callback.answer()    
