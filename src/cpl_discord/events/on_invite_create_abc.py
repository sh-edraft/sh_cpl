from abc import ABC, abstractmethod
import discord


class OnInviteCreateABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_invite_create(self, invite: discord.Invite): pass
    