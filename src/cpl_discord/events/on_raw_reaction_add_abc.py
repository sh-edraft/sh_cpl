from abc import ABC, abstractmethod
import discord
from discord import RawReactionActionEvent


class OnRawReactionAddABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        pass
