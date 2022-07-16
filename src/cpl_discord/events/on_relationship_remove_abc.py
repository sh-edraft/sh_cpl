from abc import ABC, abstractmethod
import discord


class OnRelationshipRemoveABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_relationship_remove(self, relationship: discord.Relationship): pass
