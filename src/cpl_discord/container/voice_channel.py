import discord

from cpl_discord.container.container import Container
from cpl_discord.container.member import Member
from cpl_discord.helper.to_containers_converter import ToContainersConverter
from cpl_query.extension import List


class VoiceChannel(discord.VoiceChannel, Container):

    def __init__(self, _t: discord.VoiceChannel):
        Container.__init__(self, _t, VoiceChannel)

    @property
    def members(self) -> List[Member]:
        return List(Member, ToContainersConverter.convert(self._object.members, Member))
