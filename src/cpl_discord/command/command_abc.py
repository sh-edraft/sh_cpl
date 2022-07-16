from abc import ABC, abstractmethod

from discord.ext import commands

from commands_meta import CommandsMeta


class CommandABC(ABC, commands.Cog, metaclass=CommandsMeta):

    @abstractmethod
    def __init__(self): pass
