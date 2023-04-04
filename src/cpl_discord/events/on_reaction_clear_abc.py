from abc import ABC, abstractmethod
import discord


class OnReactionClearABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_reaction_clear(self, message: discord.Message, reactions: list[discord.Reaction]):
        pass
