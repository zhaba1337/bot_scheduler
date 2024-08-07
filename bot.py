import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import random 
from aiogram import F
from aiogram.filters.callback_data import CallbackData

logging.basicConfig(level=logging.INFO)


import calendar 

bot = Bot(token="5135804286:AAEZa-5XFLKT35uc8kOMPoN6kk5hQuHPFBA")

dp = Dispatcher()

class My_cb(CallbackData, prefix='my'):
    name: str
    message_id: int
    chat_id: int
    data: str


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Нажми меня",
        callback_data="random_value")
    )
    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил число от 1 до 10",
        reply_markup=builder.as_markup()
    )

@dp.message(Command('calendar'))
async def get_calendar(message: types.Message):
    builder = InlineKeyboardBuilder()
    obj = calendar.Calendar(0).monthdays2calendar(2024, 8)
    
    print(message.message_id, message.chat.id)
    cb_next = My_cb(name = 'next', message_id=message.message_id, chat_id=message.chat.id, data='2024.08').pack()
    cb_prev = My_cb(name = 'prev', message_id=message.message_id, chat_id=message.chat.id, data='2024.08').pack()

    builder.row(
        types.InlineKeyboardButton(
                text= '<',
                callback_data=cb_prev),
        
        types.InlineKeyboardButton(
                text= 'Август',
                callback_data="qwe"),
        
        types.InlineKeyboardButton(
                text= '>',
                callback_data=cb_next)
    )
    
    builder.row(*[types.InlineKeyboardButton(text= i, callback_data="qwe") for i in ('Пн', "Вт", "Ср", "Чт", "Пт", "Сб", "Вс")])
    for i in obj:
        builder1, data = [], ''
        for j in i:
            
            if(j[0]):
                data = str(j[0])
            else:
                data = '-'
                
            builder1.append(types.InlineKeyboardButton(
                text= data,
                callback_data="qwe")
            )
                
        builder.row(*builder1)
        
        
    await message.answer(
        "Calendar",
        reply_markup=builder.as_markup()
    )            
            

@dp.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(random.randint(1, 10)))
    await callback.answer()

@dp.callback_query(My_cb.filter(F.name == 'inc'))
async def send_random_value(callback: types.CallbackQuery, callback_data: My_cb):
    await callback.message.answer(f"{callback_data}")
    await callback.answer()
    
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())