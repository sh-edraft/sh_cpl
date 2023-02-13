from abc import ABC, abstractmethod
import discord


class OnScheduledEventCreateABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_scheduled_event_create(self, event: discord.ScheduledEvent): pass
