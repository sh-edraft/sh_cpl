from abc import ABC, abstractmethod

import discord
from discord.ext import commands


class BotServiceABC(ABC, commands.Bot):

    def __init__(self):
        ABC.__init__(self)

    @abstractmethod
    async def start_async(self): pass

    @abstractmethod
    async def stop_async(self): pass
