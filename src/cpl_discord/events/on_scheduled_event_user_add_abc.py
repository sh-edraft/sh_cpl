from abc import ABC, abstractmethod
import discord


class OnScheduledEventUserAddABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_scheduled_event_user_add(self, event: discord.ScheduledEvent, user: discord.User):
        pass
