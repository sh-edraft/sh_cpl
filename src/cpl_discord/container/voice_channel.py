import discord

from cpl_discord.container.container import Container
from cpl_discord.helper.ToContainersConverter import ToContainersConverter
from cpl_query.extension import List


class VoiceChannel(discord.VoiceChannel, Container):

    def __init__(self, _t: discord.VoiceChannel):
        Container.__init__(self, _t, VoiceChannel)
