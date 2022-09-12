import discord

from cpl_discord.container.container import Container
from cpl_discord.container.member import Member
from cpl_discord.container.thread import Thread
from cpl_discord.helper.to_containers_converter import ToContainersConverter
from cpl_query.extension import List


class TextChannel(discord.TextChannel, Container):

    def __init__(self, _t: discord.TextChannel):
        Container.__init__(self, _t, TextChannel)

    @property
    def members(self) -> List[discord.Member]:
        return List(discord.Member, ToContainersConverter.convert(self._object.members, Member))

    @property
    def threads(self) -> List[Thread]:
        return List(Thread, ToContainersConverter.convert(self._object.threads, Thread))
