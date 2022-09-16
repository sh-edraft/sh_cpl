import discord

from cpl_discord.container.category_channel import CategoryChannel
from cpl_discord.container.container import Container
from cpl_discord.container.member import Member
from cpl_discord.container.role import Role
from cpl_discord.container.text_channel import TextChannel
from cpl_discord.container.voice_channel import VoiceChannel
from cpl_discord.helper.to_containers_converter import ToContainersConverter
from cpl_query.extension import List


class Guild(Container, discord.Guild):

    def __init__(self, _t: discord.Guild):
        self._object: discord.Guild = _t

        Container.__init__(self, _t, Guild)

    @property
    def categories(self) -> List[CategoryChannel]:
        return List(CategoryChannel, ToContainersConverter.convert(self._object.categories, CategoryChannel))

    @property
    def members(self) -> List[Member]:
        return List(Member, ToContainersConverter.convert(self._object.members, Member))

    @property
    def roles(self) -> List[Role]:
        return List(Role, ToContainersConverter.convert(self._object.roles, Role))

    @property
    def text_channels(self) -> List[TextChannel]:
        return List(TextChannel, ToContainersConverter.convert(self._object.text_channels, TextChannel))

    @property
    def threads(self) -> List[TextChannel]:
        return List(TextChannel, ToContainersConverter.convert(self._object.threads, TextChannel))

    @property
    def voice_channels(self) -> List[VoiceChannel]:
        return List(VoiceChannel, ToContainersConverter.convert(self._object.voice_channels, VoiceChannel))
