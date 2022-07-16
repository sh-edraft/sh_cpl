from abc import ABC, abstractmethod
import discord


class OnGuildChannelUpdateABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel): pass
