import discord

from cpl_discord.container.container import Container
from cpl_discord.container.member import Member
from cpl_discord.helper.to_containers_converter import ToContainersConverter
from cpl_query.extension import List


class Thread(discord.Thread, Container):
    def __init__(self, _t: discord.Thread):
        Container.__init__(self, _t, Thread)

    @property
    def members(self) -> List[Member]:
        return List(Member, ToContainersConverter.convert(self._object.members, Member))
