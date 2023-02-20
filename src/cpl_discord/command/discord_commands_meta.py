from abc import ABCMeta
from discord.ext import commands


class DiscordCogMeta(ABCMeta, commands.CogMeta):
    pass
