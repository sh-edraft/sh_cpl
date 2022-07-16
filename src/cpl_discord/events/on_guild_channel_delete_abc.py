from abc import ABC, abstractmethod
import discord


class OnGuildChannelDeleteABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel): pass
    