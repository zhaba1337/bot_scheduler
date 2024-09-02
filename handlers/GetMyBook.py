from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

import calendar

from db import DB_connector

from CallBacks import Admin_cb, Adm_change_year_cb

from filters.filter import IsOwner



router = Router()


@router.message(Command("mybooks"))  
async def get_busy_days_start(message: Message) -> None:
    clients_books = DB_connector().get_client_books(message.from_user.id)
    text = '\n'.join([f"{date}, {time_start}:00-{time_end}:00" for date, time_start, time_end in clients_books])
    await message.answer(text)