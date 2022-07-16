from abc import ABC, abstractmethod
import discord

class OnRelationshipAddABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_relationship_add(self, relationship: discord.Relationship): pass
    