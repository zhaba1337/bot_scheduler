from aiogram import Router
from aiogram.filters import Command
from aiogram import types
from aiogram.filters.command import Command



from db import create_connect, close_connect


router = Router()
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    con, cur = create_connect()
    if (len(cur.execute('select id from Clients WHERE telegram_id = ?', (message.from_user.id,)).fetchall()) == 0):
        cur.execute("INSERT INTO Clients (telegram_id, first_name, state_status) VALUES (?, ?, ?)", (message.from_user.id, message.from_user.username, None))
        close_connect(con)
    await message.answer("write /booking")

@router.message(Command("owner"))
async def set_new_onwer(message: types.Message):
    con, cur = create_connect()
    
    cur.execute('insert into Owners (telegram_id, username) VALUES (?, ?)', (message.from_user.id, message.from_user.username))
    close_connect(con)
    
    await message.answer('owner add!')