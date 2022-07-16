from abc import ABCMeta
from discord.ext import commands


class CommandsMeta(ABCMeta, commands.CogMeta): pass
