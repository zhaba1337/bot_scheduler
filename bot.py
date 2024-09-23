import asyncio
import logging
from aiogram import Bot, Dispatcher

from handlers import admin, booking, setWeekend, commandStart, GetBooks, GetMyBook
from db import DB_connector


logging.basicConfig(level=logging.INFO)


bot = Bot(token="5135804286:AAH3Qx_sp9VegoosjzB2-GvUIrcVLqbBPLU")

dp = Dispatcher()

async def post(bot: Bot):#post sc worker нужны хз для чего для добавления новых дней 
    
    await bot.send_message(539931122, text='qwe')

async def update_db():
    connector = DB_connector()
    connector.delete_records_before_today()
    connector.delete_datetimes_before_today()
    connector.insert_datetime_slots()


async def sc():
    while True:
        await post(bot=bot)
        await update_db()
        await asyncio.sleep(86400)
        

def worker():
    asyncio.run(((sc())))
    
async def main():
    from multiprocessing import Process
    process = Process(target=worker)
    process.start()
    
    dp.include_routers(
        admin.router,
        setWeekend.router,
        commandStart.router,
        GetBooks.router,
        booking.router,
        GetMyBook.router,
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())