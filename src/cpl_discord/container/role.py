import discord

from cpl_discord.container.container import Container

from cpl_discord.helper.to_containers_converter import ToContainersConverter
from cpl_query.extension.list import List


class Role(discord.Role, Container):
    def __init__(self, _t: discord.Role):
        Container.__init__(self, _t, Role)

    @property
    def members(self) -> List["Member"]:
        from cpl_discord.container.member import Member

        return List(Member, ToContainersConverter.convert(self._object.members, Member))
