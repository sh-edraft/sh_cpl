from enum import Enum

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


class EventTypesEnum(Enum):
    on_ready = OnReadyABC
    on_bulk_message_delete_abc = OnBulkMessageDeleteABC
    on_connect_abc = OnConnectABC
    on_disconnect_abc = OnDisconnectABC
    on_group_join_abc = OnGroupJoinABC
    on_group_remove_abc = OnGroupRemoveABC
    on_guild_available_abc = OnGuildAvailableABC
    on_guild_channel_create_abc = OnGuildChannelCreateABC
    on_guild_channel_delete_abc = OnGuildChannelDeleteABC
    on_guild_channel_pins_update_abc = OnGuildChannelPinsUpdateABC
    on_guild_channel_update_abc = OnGuildChannelUpdateABC
    on_guild_emojis_update_abc = OnGuildEmojisUpdateABC
    on_guild_integrations_update_abc = OnGuildIntegrationsUpdateABC
    on_guild_join_abc = OnGuildJoinABC
    on_guild_remove_abc = OnGuildRemoveABC
    on_guild_role_create_abc = OnGuildRoleCreateABC
    on_guild_role_delete_abc = OnGuildRoleDeleteABC
    on_guild_role_update_abc = OnGuildRoleUpdateABC
    on_guild_unavailable_abc = OnGuildUnavailableABC
    on_guild_update_abc = OnGuildUpdateABC
    on_invite_create_abc = OnInviteCreateABC
    on_invite_delete_abc = OnInviteDeleteABC
    on_member_ban_abc = OnMemberBanABC
    on_member_join_abc = OnMemberJoinABC
    on_member_remove_abc = OnMemberRemoveABC
    on_member_unban_abc = OnMemberUnbanABC
    on_member_update_abc = OnMemberUpdateABC
    on_message_abc = OnMessageABC
    on_message_delete_abc = OnMessageDeleteABC
    on_message_edit_abc = OnMessageEditABC
    on_private_channel_create_abc = OnPrivateChannelCreateABC
    on_private_channel_delete_abc = OnPrivateChannelDeleteABC
    on_private_channel_pins_update_abc = OnPrivateChannelPinsUpdateABC
    on_private_channel_update_abc = OnPrivateChannelUpdateABC
    on_reaction_add_abc = OnReactionAddABC
    on_reaction_clear_abc = OnReactionClearABC
    on_reaction_clear_emoji_abc = OnReactionClearEmojiABC
    on_reaction_remove_abc = OnReactionRemoveABC
    on_ready_abc = OnReadyABC
    on_relationship_add_abc = OnRelationshipAddABC
    on_relationship_remove_abc = OnRelationshipRemoveABC
    on_relationship_update_abc = OnRelationshipUpdateABC
    on_resume_abc = OnResumeABC
    on_typing_abc = OnTypingABC
    on_user_update_abc = OnUserUpdateABC
    on_voice_state_update_abc = OnVoiceStateUpdateABC
    on_webhooks_update_abc = OnWebhooksUpdateABC
