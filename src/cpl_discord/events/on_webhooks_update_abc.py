from abc import ABC, abstractmethod
import discord


class OnWebhooksUpdateABC(ABC):

    @abstractmethod
    def __init__(self): pass


    @abstractmethod
    async def on_webhooks_update(self, channel: discord.abc.GuildChannel): pass
