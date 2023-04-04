from abc import ABC, abstractmethod
import discord


class OnReactionClearEmojiABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_reaction_clear_emoji(self, reaction: discord.Reaction):
        pass
