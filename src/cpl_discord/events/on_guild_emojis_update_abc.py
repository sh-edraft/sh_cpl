from abc import ABC, abstractmethod
from typing import Sequence
import discord


class OnGuildEmojisUpdateABC(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def on_guild_emojis_update(
        self, guild: discord.Guild, before: Sequence[discord.Emoji], after: Sequence[discord.Emoji]
    ):
        pass
