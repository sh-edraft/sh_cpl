from abc import ABC, abstractmethod
import discord
from discord import RawReactionActionEvent


class OnRawReactionRemoveABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent): pass
    