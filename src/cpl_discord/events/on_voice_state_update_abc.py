from abc import ABC, abstractmethod
import discord


class OnVoiceStateUpdateABC(ABC):

    @abstractmethod
    def __init__(self): pass

    @abstractmethod
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState,after: discord.VoiceState): pass
