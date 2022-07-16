from abc import ABC, abstractmethod

from discord.ext import commands

from discord_commands_meta import DiscordCogMeta


class DiscordCommandABC(ABC, commands.Cog, metaclass=DiscordCogMeta):

    @abstractmethod
    def __init__(self): pass
