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


@router.message(IsOwner(), Command("getbooks"))  
async def get_busy_days_start(message: Message) -> None:
    books = DB_connector().get_all_books()
    text = '\n'.join([f"@{username}, {date}, {time_start}:00-{time_end}:00" for username, date, time_start, time_end in books])
    await message.answer(text)