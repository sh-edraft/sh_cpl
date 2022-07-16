from datetime import datetime
from typing import Optional, Sequence, Union, Type

import discord
from discord.ext import commands

from cpl_core.console import Console
from cpl_core.dependency_injection import ServiceProviderABC
from cpl_core.logging import LoggerABC
from cpl_core.utils import String
from cpl_discord.command.discord_commands_meta import DiscordCogMeta
from cpl_discord.events.on_bulk_message_delete_abc import OnBulkMessageDeleteABC
from cpl_discord.events.on_connect_abc import OnConnectABC
from cpl_discord.events.on_disconnect_abc import OnDisconnectABC
from cpl_discord.events.on_group_join_abc import OnGroupJoinABC
from cpl_discord.events.on_group_remove_abc import OnGroupRemoveABC
from cpl_discord.events.on_guild_available_abc import OnGuildAvailableABC
from cpl_discord.events.on_guild_channel_create_abc import OnGuildChannelCreateABC
from cpl_discord.events.on_guild_channel_delete_abc import OnGuildChannelDeleteABC
from cpl_discord.events.on_guild_channel_pins_update_abc import OnGuildChannelPinsUpdateABC
from cpl_discord.events.on_guild_channel_update_abc import OnGuildChannelUpdateABC
from cpl_discord.events.on_guild_emojis_update_abc import OnGuildEmojisUpdateABC
from cpl_discord.events.on_guild_integrations_update_abc import OnGuildIntegrationsUpdateABC
from cpl_discord.events.on_guild_join_abc import OnGuildJoinABC
from cpl_discord.events.on_guild_remove_abc import OnGuildRemoveABC
from cpl_discord.events.on_guild_role_create_abc import OnGuildRoleCreateABC
from cpl_discord.events.on_guild_role_delete_abc import OnGuildRoleDeleteABC
from cpl_discord.events.on_guild_role_update_abc import OnGuildRoleUpdateABC
from cpl_discord.events.on_guild_unavailable_abc import OnGuildUnavailableABC
from cpl_discord.events.on_guild_update_abc import OnGuildUpdateABC
from cpl_discord.events.on_invite_create_abc import OnInviteCreateABC
from cpl_discord.events.on_invite_delete_abc import OnInviteDeleteABC
from cpl_discord.events.on_member_ban_abc import OnMemberBanABC
from cpl_discord.events.on_member_join_abc import OnMemberJoinABC
from cpl_discord.events.on_member_remove_abc import OnMemberRemoveABC
from cpl_discord.events.on_member_unban_abc import OnMemberUnbanABC
from cpl_discord.events.on_member_update_abc import OnMemberUpdateABC
from cpl_discord.events.on_message_abc import OnMessageABC
from cpl_discord.events.on_message_delete_abc import OnMessageDeleteABC
from cpl_discord.events.on_message_edit_abc import OnMessageEditABC
from cpl_discord.events.on_private_channel_create_abc import OnPrivateChannelCreateABC
from cpl_discord.events.on_private_channel_delete_abc import OnPrivateChannelDeleteABC
from cpl_discord.events.on_private_channel_pins_update_abc import OnPrivateChannelPinsUpdateABC
from cpl_discord.events.on_private_channel_update_abc import OnPrivateChannelUpdateABC
from cpl_discord.events.on_reaction_add_abc import OnReactionAddABC
from cpl_discord.events.on_reaction_clear_abc import OnReactionClearABC
from cpl_discord.events.on_reaction_clear_emoji_abc import OnReactionClearEmojiABC
from cpl_discord.events.on_reaction_remove_abc import OnReactionRemoveABC
from cpl_discord.events.on_ready_abc import OnReadyABC
from cpl_discord.events.on_relationship_add_abc import OnRelationshipAddABC
from cpl_discord.events.on_relationship_remove_abc import OnRelationshipRemoveABC
from cpl_discord.events.on_relationship_update_abc import OnRelationshipUpdateABC
from cpl_discord.events.on_resume_abc import OnResumeABC
from cpl_discord.events.on_typing_abc import OnTypingABC
from cpl_discord.events.on_user_update_abc import OnUserUpdateABC
from cpl_discord.events.on_voice_state_update_abc import OnVoiceStateUpdateABC
from cpl_discord.events.on_webhooks_update_abc import OnWebhooksUpdateABC
from cpl_discord.service.discord_collection_abc import DiscordCollectionABC
from cpl_discord.service.discord_service_abc import DiscordServiceABC


class DiscordService(DiscordServiceABC, commands.Cog, metaclass=DiscordCogMeta):

    def __init__(
            self,
            logger: LoggerABC,
            dc_collection: DiscordCollectionABC,
            services: ServiceProviderABC
    ):
        DiscordServiceABC.__init__(self)
        self._logger = logger
        self._collection = dc_collection
        self._services = services

    async def _handle_event(self, event: Type, *args):
        event_collection = self._collection.get_events_by_base(event)
        if event_collection is None:
            return

        for event_type in event_collection:
            event_instance = self._services.get_service(event_type)

            func_name = event.__name__
            if func_name.endswith('ABC'):
                func_name = func_name.replace('ABC', '')

            func_name = String.convert_to_snake_case(func_name)

            try:
                func = getattr(event_instance, func_name)
                await func(*args)
            except Exception as e:
                self._logger.error(__name__, f'Cannot execute {func_name} of {event_instance.__name__}', e)

    @commands.Cog.listener()
    async def on_connect(self):
        self._logger.trace(__name__, f'Received on_connect')
        await self._handle_event(OnConnectABC)

    @commands.Cog.listener()
    async def on_disconnect(self):
        self._logger.trace(__name__, f'Received on_disconnect')
        await self._handle_event(OnDisconnectABC)

    async def on_ready(self):
        self._logger.trace(__name__, f'Received on_ready')
        await self._handle_event(OnReadyABC)

    @commands.Cog.listener()
    async def on_resume(self):
        self._logger.trace(__name__, f'Received on_resume')
        await self._handle_event(OnResumeABC)

    @commands.Cog.listener()
    async def on_error(self, event: str, *args, **kwargs):
        self._logger.trace(__name__, f'Received on_error:\n\t{event}\n\t{args}\n\t{kwargs}')
        await self._handle_event(OnReadyABC, event, *args, **kwargs)

    @commands.Cog.listener()
    async def on_typing(self, channel: discord.abc.Messageable, user: Union[discord.User, discord.Member], when: datetime):
        self._logger.trace(__name__, f'Received on_typing:\n\t{channel}\n\t{user}\n\t{when}')
        await self._handle_event(OnTypingABC, channel, user, when)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        self._logger.trace(__name__, f'Received on_message:\n\t{message}\n\t{message.content}')
        await self._handle_event(OnMessageABC, message)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        self._logger.trace(__name__, f'Received on_message_delete:\n\t{message}\n\t{message.content}')
        await self._handle_event(OnMessageDeleteABC, message)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages: list[discord.Message]):
        self._logger.trace(__name__, f'Received on_bulk_message_delete:\n\t{len(messages)}')
        await self._handle_event(OnBulkMessageDeleteABC, messages)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        self._logger.trace(__name__, f'Received on_message_edit:\n\t{before}\n\t{after}')
        await self._handle_event(OnMessageEditABC, before, after)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        self._logger.trace(__name__, f'Received on_reaction_add:\n\t{reaction}\n\t{user}')
        await self._handle_event(OnReactionAddABC, reaction, user)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.User):
        self._logger.trace(__name__, f'Received on_reaction_remove:\n\t{reaction}\n\t{user}')
        await self._handle_event(OnReactionRemoveABC, reaction, user)

    @commands.Cog.listener()
    async def on_reaction_clear(self, message: discord.Message, reactions: list[discord.Reaction]):
        self._logger.trace(__name__, f'Received on_reaction_reon_reaction_clearmove:\n\t{message}\n\t{len(reactions)}')
        await self._handle_event(OnReactionClearABC, message, reactions)

    @commands.Cog.listener()
    async def on_reaction_clear_emoji(self, reaction: discord.Reaction):
        self._logger.trace(__name__, f'Received on_reaction_clear_emoji:\n\t{reaction}')
        await self._handle_event(OnReactionClearEmojiABC, reaction)

    @commands.Cog.listener()
    async def on_private_channel_delete(self, channel: discord.abc.PrivateChannel):
        self._logger.trace(__name__, f'Received on_private_channel_delete:\n\t{channel}')
        await self._handle_event(OnPrivateChannelDeleteABC, channel)

    @commands.Cog.listener()
    async def on_private_channel_create(self, channel: discord.abc.PrivateChannel):
        self._logger.trace(__name__, f'Received on_private_channel_create:\n\t{channel}')
        await self._handle_event(OnPrivateChannelCreateABC, channel)

    @commands.Cog.listener()
    async def on_private_channel_update(self, before: discord.GroupChannel, after: discord.GroupChannel):
        self._logger.trace(__name__, f'Received on_private_channel_update:\n\t{before}\n\t{after}')
        await self._handle_event(OnPrivateChannelUpdateABC, before, after)

    @commands.Cog.listener()
    async def on_private_channel_pins_update(self, channel: discord.abc.PrivateChannel, list_pin: Optional[datetime]):
        self._logger.trace(__name__, f'Received on_private_channel_pins_update:\n\t{channel}\n\t{list_pin}')
        await self._handle_event(OnPrivateChannelPinsUpdateABC, channel, list_pin)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: discord.abc.GuildChannel):
        self._logger.trace(__name__, f'Received on_guild_channel_delete:\n\t{channel}')
        await self._handle_event(OnGuildChannelDeleteABC, channel)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: discord.abc.GuildChannel):
        self._logger.trace(__name__, f'Received on_guild_channel_create:\n\t{channel}')
        await self._handle_event(OnGuildChannelCreateABC, channel)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: discord.abc.GuildChannel, after: discord.abc.GuildChannel):
        self._logger.trace(__name__, f'Received on_guild_channel_update:\n\t{before}\n\t{after}')
        await self._handle_event(OnGuildChannelUpdateABC, before, after)

    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel: discord.abc.GuildChannel, list_pin: Optional[datetime]):
        self._logger.trace(__name__, f'Received on_guild_channel_pins_update:\n\t{channel}\n\t{list_pin}')
        await self._handle_event(OnGuildChannelPinsUpdateABC, channel, list_pin)

    @commands.Cog.listener()
    async def on_guild_integrations_update(self, guild: discord.Guild):
        self._logger.trace(__name__, f'Received on_guild_integrations_update:\n\t{guild}')
        await self._handle_event(OnGuildIntegrationsUpdateABC, guild)

    @commands.Cog.listener()
    async def on_webhooks_update(self, channel: discord.abc.GuildChannel):
        self._logger.trace(__name__, f'Received on_webhooks_update:\n\t{channel}')
        await self._handle_event(OnWebhooksUpdateABC, channel)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        self._logger.trace(__name__, f'Received on_member_join:\n\t{member}')
        await self._handle_event(OnMemberJoinABC, member)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        self._logger.trace(__name__, f'Received on_member_remove:\n\t{member}')
        await self._handle_event(OnMemberRemoveABC, member)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        self._logger.trace(__name__, f'Received on_member_update:\n\t{before}\n\t{after}')
        await self._handle_event(OnMemberUpdateABC, before, after)

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        self._logger.trace(__name__, f'Received on_user_update:\n\t{before}\n\t{after}')
        await self._handle_event(OnUserUpdateABC, before, after)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        self._logger.trace(__name__, f'Received on_guild_join:\n\t{guild}')
        await self._handle_event(OnGuildJoinABC, guild)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        self._logger.trace(__name__, f'Received on_guild_remove:\n\t{guild}')
        await self._handle_event(OnGuildRemoveABC, guild)

    @commands.Cog.listener()
    async def on_guild_update(self, before: discord.Guild, after: discord.Guild):
        self._logger.trace(__name__, f'Received on_guild_update:\n\t{before}\n\t{after}')
        await self._handle_event(OnGuildUpdateABC, before, after)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role: discord.Role):
        self._logger.trace(__name__, f'Received on_guild_role_create:\n\t{role}')
        await self._handle_event(OnGuildRoleCreateABC, role)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        self._logger.trace(__name__, f'Received on_guild_role_delete:\n\t{role}')
        await self._handle_event(OnGuildRoleDeleteABC, role)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        self._logger.trace(__name__, f'Received on_guild_role_update:\n\t{before}\n\t{after}')
        await self._handle_event(OnGuildRoleUpdateABC, before, after)

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild: discord.Guild, before: Sequence[discord.Emoji], after: Sequence[discord.Emoji]):
        self._logger.trace(__name__, f'Received on_guild_emojis_update:\n\t{guild}\n\t{before}\n\t{after}')
        await self._handle_event(OnGuildEmojisUpdateABC, guild, before, after)

    @commands.Cog.listener()
    async def on_guild_available(self, guild: discord.Guild):
        self._logger.trace(__name__, f'Received on_guild_available:\n\t{guild}')
        await self._handle_event(OnGuildAvailableABC, guild)

    @commands.Cog.listener()
    async def on_guild_unavailable(self, guild: discord.Guild):
        self._logger.trace(__name__, f'Received on_guild_unavailable:\n\t{guild}')
        await self._handle_event(OnGuildUnavailableABC, guild)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        self._logger.trace(__name__, f'Received on_voice_state_update:\n\t{member}\n\t{before}\n\t{after}')
        await self._handle_event(OnVoiceStateUpdateABC, member, before, after)

    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.User):
        self._logger.trace(__name__, f'Received on_member_ban:\n\t{guild}\n\t{user}')
        await self._handle_event(OnMemberBanABC, guild, user)

    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.User):
        self._logger.trace(__name__, f'Received on_member_unban:\n\t{guild}\n\t{user}')
        await self._handle_event(OnMemberUnbanABC, guild, user)

    @commands.Cog.listener()
    async def on_invite_create(self, invite: discord.Invite):
        self._logger.trace(__name__, f'Received on_invite_create:\n\t{invite}')
        await self._handle_event(OnInviteCreateABC, invite)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite: discord.Invite):
        self._logger.trace(__name__, f'Received on_invite_create:\n\t{invite}')
        await self._handle_event(OnInviteDeleteABC, invite)

    @commands.Cog.listener()
    async def on_group_join(self, channel: discord.GroupChannel, user: discord.User):
        self._logger.trace(__name__, f'Received on_group_join:\n\t{channel}\n\t{user}')
        await self._handle_event(OnGroupJoinABC, channel, user)

    @commands.Cog.listener()
    async def on_group_remove(self, channel: discord.GroupChannel, user: discord.User):
        self._logger.trace(__name__, f'Received on_group_remove:\n\t{channel}\n\t{user}')
        await self._handle_event(OnGroupRemoveABC, channel, user)

    @commands.Cog.listener()
    async def on_relationship_add(self, relationship: discord.Relationship):
        self._logger.trace(__name__, f'Received on_relationship_add:\n\t{relationship}')
        await self._handle_event(OnRelationshipAddABC, relationship)

    @commands.Cog.listener()
    async def on_relationship_remove(self, relationship: discord.Relationship):
        self._logger.trace(__name__, f'Received on_relationship_remove:\n\t{relationship}')
        await self._handle_event(OnRelationshipRemoveABC, relationship)

    @commands.Cog.listener()
    async def on_relationship_update(self, before: discord.Relationship, after: discord.Relationship):
        self._logger.trace(__name__, f'Received on_relationship_update:\n\t{before}\n\t{after}')
        await self._handle_event(OnRelationshipUpdateABC, before, after)
