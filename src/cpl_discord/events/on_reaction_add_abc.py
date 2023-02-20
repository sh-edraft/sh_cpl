from abc import ABC, abstractmethod
import discord


class OnReactionAddABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        pass
