from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
import discord


class OnPrivateChannelPinsUpdateABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_private_channel_pins_update(self, channel: discord.abc.PrivateChannel, list_pin: Optional[datetime]):
        pass
