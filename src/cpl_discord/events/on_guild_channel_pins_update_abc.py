from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
import discord


class OnGuildChannelPinsUpdateABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_guild_channel_pins_update(self, channel: discord.abc.GuildChannel, list_pin: Optional[datetime]):
        pass
