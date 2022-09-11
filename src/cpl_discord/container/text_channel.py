import discord

from cpl_discord.container.container import Container
from cpl_discord.helper.ToContainersConverter import ToContainersConverter
from cpl_query.extension import List


class TextChannel(discord.TextChannel, Container):

    def __init__(self, _t: discord.TextChannel):
        Container.__init__(self, _t, TextChannel)
