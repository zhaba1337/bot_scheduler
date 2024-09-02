from typing import Any
from aiogram.filters import BaseFilter
from aiogram.types import Message

from db import DB_connector

class IsOwner(BaseFilter):
    def __init__(self) -> None:
        self.owner_id = DB_connector().get_owner_id()
        
    async def __call__(self, message: Message) -> Any:
        return message.from_user.id == self.owner_id