from abc import ABC, abstractmethod
from datetime import datetime
from typing import Union
import discord


class OnTypingABC(ABC):

    @abstractmethod
    def __init__(self): pass
    
    @abstractmethod
    async def on_typing(self, channel: discord.abc.Messageable, user: Union[discord.User, discord.Member], when: datetime): pass
