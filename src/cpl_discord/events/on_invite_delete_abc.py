from abc import ABC, abstractmethod
import discord


class OnInviteDeleteABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_invite_delete(self, invite: discord.Invite): pass
