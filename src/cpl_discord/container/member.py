import discord

from cpl_discord.container.container import Container
from cpl_discord.helper.to_containers_converter import ToContainersConverter
from cpl_query.extension.list import List


class Member(discord.Member, Container):

    def __init__(self, _t: discord.Member):
        Container.__init__(self, _t, Member)

    @property
    def roles(self) -> List['Role']:
        from cpl_discord.container.role import Role
        return List(Role, ToContainersConverter.convert(self._object.roles, Role))
