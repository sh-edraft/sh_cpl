from abc import ABC, abstractmethod
import discord


class OnGuildChannelCreateABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel): pass
    