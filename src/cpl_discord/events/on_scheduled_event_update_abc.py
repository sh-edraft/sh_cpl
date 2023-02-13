from abc import ABC, abstractmethod
import discord


class OnScheduledEventUpdateABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_scheduled_event_update(self, before: discord.ScheduledEvent, after: discord.ScheduledEvent): pass
