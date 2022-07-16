from abc import ABC, abstractmethod

import discord
from discord.ext import commands


class DiscordBotServiceABC(commands.Bot):

    def __init__(self, **kwargs):
        commands.Bot.__init__(self, **kwargs)

    @abstractmethod
    async def start_async(self): pass

    @abstractmethod
    async def stop_async(self): pass

    @abstractmethod
    async def on_ready(self): pass
