from abc import ABC, abstractmethod
import discord


class OnScheduledEventDeleteABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_scheduled_event_delete(self, event: discord.ScheduledEvent):
        pass
