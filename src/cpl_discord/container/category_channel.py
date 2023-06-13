import discord

from cpl_discord.container.container import Container
from cpl_discord.container.text_channel import TextChannel
from cpl_discord.container.voice_channel import VoiceChannel
from cpl_discord.helper.to_containers_converter import ToContainersConverter
from cpl_query.extension.list import List


class CategoryChannel(discord.CategoryChannel, Container):
    def __init__(self, _t: discord.CategoryChannel):
        Container.__init__(self, _t, CategoryChannel)

    @property
    def text_channels(self) -> List[TextChannel]:
        return List(TextChannel, ToContainersConverter.convert(self._object.text_channels, TextChannel))

    @property
    def voice_channels(self) -> List[VoiceChannel]:
        return List(VoiceChannel, ToContainersConverter.convert(self._object.voice_channels, VoiceChannel))
