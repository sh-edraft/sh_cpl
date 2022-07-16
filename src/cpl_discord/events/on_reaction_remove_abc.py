from abc import ABC, abstractmethod
import discord


class OnReactionRemoveABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User): pass
    