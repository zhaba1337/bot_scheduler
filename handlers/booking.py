from aiogram import Router, F
from aiogram.filters import Command
from aiogram import types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot import Bot

from datetime import datetime
from aiogram.fsm.context import FSMContext


from db import DB_connector
from sup_function import create_calendar, prev_month, next_month
from CallBacks import CB_booking
from kbs.ikb_calendar import kb_builder_calendar, ikb_new, ikb_builder_owner_accept_reject, ikb_builder_owner_comment, ikb_builder_time_slots
from states.comments import FSMComment

router = Router()

@router.message(Command('booking'))
async def start_booking(message: types.Message):

    year = datetime.now().year
    month = datetime.now().month

    CB_next_month = CB_booking(name = 'next_month', date=f"{year}-{month}").pack()
    builder = kb_builder_calendar(year, month, 'empty', CB_next_month)
    
    await message.answer('Пожалуйста выберите число:', reply_markup=builder.as_markup())


@router.callback_query(CB_booking.filter(F.name == 'next_month'))
async def next_month_calendar(callback: types.CallbackQuery, callback_data: CB_booking):
    date = next_month(datetime.strptime(callback_data.date, '%Y-%m'))
    year = date.year
    month = date.month
    
    CB_next_month = CB_booking(name = 'next_month', date=f"{year}-{month}").pack()
    CB_prev_month = CB_booking(name = 'prev_month', date=f"{year}-{month}").pack()
    #if (datetime(year, month, 1) <)
    
    builder = kb_builder_calendar(year, month, CB_prev_month, 'empty')
    
    await callback.message.edit_text('Пожалуйста выберите число:', reply_markup=builder.as_markup())
     
      
@router.callback_query(CB_booking.filter(F.name == 'prev_month'))
async def prev_month_calendar(callback: types.CallbackQuery, callback_data: CB_booking):
    date = prev_month(datetime.strptime(callback_data.date, '%Y-%m'))
    year = date.year
    month = date.month

    CB_next_month = CB_booking(name = 'next_month', date=f"{year}-{month}").pack()
    CB_prev_month = CB_booking(name = 'prev_month', date=f"{year}-{month}").pack()
    builder = kb_builder_calendar(year, month, 'empty', CB_next_month)
    
    await callback.message.edit_text('Пожалуйста выберите число:', reply_markup=builder.as_markup())
     
     
@router.callback_query(CB_booking.filter(F.name == 'choice_time_slot'))
async def select_time_edit_message(callback: types.CallbackQuery, callback_data: CB_booking):

    builder = ikb_builder_time_slots(date=callback_data.date)

    await callback.message.edit_text(text=f"Выберите время которое вас интересует:", reply_markup=builder.as_markup())

    await callback.answer()
    

    
@router.callback_query(CB_booking.filter(F.name == 'accept_data'))
async def select_time_edit_message(callback: types.CallbackQuery, callback_data: CB_booking):

    cb_accept = CB_booking(name='send_book_to_owner', date=callback_data.date, time_slot=callback_data.time_slot, client_username=DB_connector().get_user_name(callback.message.chat.id)).pack()
    cb_back = CB_booking(name='choice_time_slot', date=callback_data.date).pack()
    builder = InlineKeyboardBuilder().row(ikb_new('Принять', cb_accept), ikb_new('Назад', cb_back))
    await callback.message.edit_text(text=f'проверьте данные, если всё верно подтвердите заявку.\n{callback_data.for_client()}', reply_markup=builder.as_markup())
    

@router.callback_query(CB_booking.filter(F.name == 'send_book_to_owner'))
async def select_time_edit_message(callback: types.CallbackQuery, callback_data: CB_booking, bot: Bot):
    await callback.message.edit_text(text='Хорошо ожидайте ответа!')
    owner_tg_id = DB_connector().get_owner_id()
    
    await bot.send_message(owner_tg_id, text=f'FOR OWNER:\n{callback_data.for_owner()}', reply_markup=ikb_builder_owner_accept_reject(*callback_data.for_accept_bid()).as_markup())


@router.callback_query(CB_booking.filter(F.name == 'accept_bid'))
async def accept_bid(callback: types.CallbackQuery, callback_data: CB_booking, bot: Bot):
    connector = DB_connector() 
    connector.insert_record(connector.get_telegram_id(callback_data.client_username), callback_data.date, callback_data.time_slot)
    await callback.message.edit_text(text=f"Оставить комментарий для @{callback_data.client_username}?\n{callback_data.for_owner()}", reply_markup=ikb_builder_owner_comment(callback_data.client_username).as_markup())
    await bot.send_message(chat_id=connector.get_telegram_id(callback_data.client_username), text=f"Ваша Заявка принята!\n{callback_data.for_client()} \nМожете связаться: @{DB_connector().get_owner_username()}")
    await callback.answer()
    
    
@router.callback_query(CB_booking.filter(F.name == 'reject_bid'))
async def accept_bid(callback: types.CallbackQuery, callback_data: CB_booking, bot: Bot):
    await callback.message.edit_text(text=f"заявка отклонена!\n{callback_data.for_owner()}")
    await bot.send_message(chat_id=DB_connector().get_telegram_id(callback_data.client_username), text=f"Заявка отклонена!\n{callback_data.for_client()}")
    await callback.answer()
    
    
@router.callback_query(CB_booking.filter(F.name == 'accept_comment'))
async def accept_bid(callback: types.CallbackQuery, callback_data: CB_booking, state: FSMContext):
    
    await state.set_state(FSMComment.user_id)   
    await state.update_data(user_id = DB_connector().get_telegram_id(callback_data.client_username))
    await state.set_state(FSMComment.comment) 
    await callback.message.edit_text(text=f"{callback_data.for_owner()}\nНапишите комментарий для @{callback_data.client_username}:")
    

    
@router.message(FSMComment.comment)
async def accept_bid(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    await bot.send_message(chat_id=data['user_id'], text=f"Комментарий: {message.text}")
    await message.answer('Комментарий доставлен!')
    
    
    
@router.callback_query(CB_booking.filter(F.name == 'reject_comment'))
async def accept_bid(callback: types.CallbackQuery, callback_data: CB_booking):
    await callback.message.answer('запись окончена!')
    await callback.answer()