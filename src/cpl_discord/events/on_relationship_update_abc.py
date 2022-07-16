from abc import ABC, abstractmethod
import discord


class OnRelationshipUpdateABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_relationship_update(
        self, before: discord.Relationship, after: discord.Relationship): pass
