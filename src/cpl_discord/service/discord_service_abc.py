from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Sequence, Union

import discord
from discord.ext import commands


class DiscordServiceABC(ABC):

    def __init__(self):
        ABC.__init__(self)

    @abstractmethod
    def init(self, bot: commands.Bot): pass

    @abstractmethod
    async def on_connect(self): pass

    @abstractmethod
    async def on_command(self): pass

    @abstractmethod
    async def on_command_error(self): pass

    @abstractmethod
    async def on_command_completion(self): pass

    @abstractmethod
    async def on_disconnect(self): pass

    @abstractmethod
    async def on_error(self, event: str, *args, **kwargs): pass

    @abstractmethod
    async def on_ready(self): pass

    @abstractmethod
    async def on_resume(self): pass

    @abstractmethod
    async def on_error(self, event: str, *args, **kwargs): pass

    @abstractmethod
    async def on_typing(self, channel: discord.abc.Messageable, user: Union[discord.User, discord.Member], when: datetime): pass

    @abstractmethod
    async def on_message(self, message: discord.Message): pass

    @abstractmethod
    async def on_message_delete(self, message: discord.Message): pass

    @abstractmethod
    async def on_bulk_message_delete(self, messages: list[discord.Message]): pass

    @abstractmethod
    async def on_message_edit(self, before: discord.Message, after: discord.Message): pass

    @abstractmethod
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User): pass

    @abstractmethod
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User): pass

    @abstractmethod
    async def on_reaction_clear(self, message: discord.Message, reactions: list[discord.Reaction]): pass

    @abstractmethod
    async def on_reaction_clear_emoji(self, reaction: discord.Reaction): pass

    @abstractmethod
    async def on_private_channel_delete(self, channel: discord.abc.PrivateChannel): pass

    @abstractmethod
    async def on_private_channel_create(self, channel: discord.abc.PrivateChannel): pass

    @abstractmethod
    async def on_private_channel_update(self, before: discord.GroupChannel, after: discord.GroupChannel): pass

    @abstractmethod
    async def on_private_channel_pins_update(self, channel: discord.abc.PrivateChannel, list_pin: Optional[datetime]): pass

    @abstractmethod
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel): pass

    @abstractmethod
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel): pass

    @abstractmethod
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel): pass

    @abstractmethod
    async def on_guild_channel_pins_update(self, channel: discord.abc.GuildChannel, list_pin: Optional[datetime]): pass

    @abstractmethod
    async def on_guild_integrations_update(self, guild: discord.Guild): pass

    @abstractmethod
    async def on_webhooks_update(self, channel: discord.abc.GuildChannel): pass

    @abstractmethod
    async def on_member_join(self, member: discord.Member): pass

    @abstractmethod
    async def on_member_remove(self, member: discord.Member): pass

    @abstractmethod
    async def on_member_update(self, before: discord.Member, after: discord.Member): pass

    @abstractmethod
    async def on_user_update(self, before: discord.User, after: discord.User): pass

    @abstractmethod
    async def on_guild_join(self, guild: discord.Guild): pass

    @abstractmethod
    async def on_guild_remove(self, guild: discord.Guild): pass

    @abstractmethod
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild): pass

    @abstractmethod
    async def on_guild_role_create(self, role: discord.Role): pass

    @abstractmethod
    async def on_guild_role_delete(self, role: discord.Role): pass

    @abstractmethod
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role): pass

    @abstractmethod
    async def on_guild_emojis_update(self, guild: discord.Guild, before: Sequence[discord.Emoji], after: Sequence[discord.Emoji]): pass

    @abstractmethod
    async def on_guild_available(self, guild: discord.Guild): pass

    @abstractmethod
    async def on_guild_unavailable(self, guild: discord.Guild): pass

    @abstractmethod
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState): pass

    @abstractmethod
    async def on_member_ban(self, guild: discord.Guild, user: discord.User): pass

    @abstractmethod
    async def on_member_unban(self, guild: discord.Guild, user: discord.User): pass

    @abstractmethod
    async def on_invite_create(self, invite: discord.Invite): pass

    @abstractmethod
    async def on_invite_delete(self, invite: discord.Invite): pass

    @abstractmethod
    async def on_group_join(self, chhanel: discord.GroupChannel, user: discord.User): pass

    @abstractmethod
    async def on_group_remove(self, chhanel: discord.GroupChannel, user: discord.User): pass

    @abstractmethod
    async def on_relationship_add(self, relationship: discord.Relationship): pass

    @abstractmethod
    async def on_relationship_remove(self, relationship: discord.Relationship): pass

    @abstractmethod
    async def on_relationship_update(self, before: discord.Relationship, after: discord.Relationship): pass
