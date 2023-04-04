from abc import ABC, abstractmethod
import discord
from discord import RawReactionActionEvent


class OnRawReactionClearEmojiABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_raw_reaction_clear_emoji(self, payload: RawReactionActionEvent):
        pass
