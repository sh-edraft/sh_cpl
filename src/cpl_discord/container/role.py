import discord

from cpl_discord.container.container import Container
from cpl_discord.container.member import Member
from cpl_discord.helper.ToContainersConverter import ToContainersConverter
from cpl_query.extension import List


class Role(discord.Role, Container):

    def __init__(self, _t: discord.Role):
        Container.__init__(self, _t, Role)

    @property
    def members(self) -> List[discord.Member]:
        return List(discord.Member, ToContainersConverter.convert(self._object.members, Member))
