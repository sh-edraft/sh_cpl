# -*- coding: utf-8 -*-

"""
cpl-discord sh-edraft Common Python library Discord
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library link between discord.py and CPL

:copyright: (c) 2021 - 2022 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_discord.events'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2021 - 2022 sh-edraft.de'
__version__ = '2022.7.0.post4'

from collections import namedtuple


# imports:
from .on_bulk_message_delete_abc import OnBulkMessageDeleteABC
from .on_command_abc import OnCommandABC
from .on_command_completion_abc import OnCommandCompletionABC
from .on_command_error_abc import OnCommandErrorABC
from .on_connect_abc import OnConnectABC
from .on_disconnect_abc import OnDisconnectABC
from .on_group_join_abc import OnGroupJoinABC
from .on_group_remove_abc import OnGroupRemoveABC
from .on_guild_available_abc import OnGuildAvailableABC
from .on_guild_channel_create_abc import OnGuildChannelCreateABC
from .on_guild_channel_delete_abc import OnGuildChannelDeleteABC
from .on_guild_channel_pins_update_abc import OnGuildChannelPinsUpdateABC
from .on_guild_channel_update_abc import OnGuildChannelUpdateABC
from .on_guild_emojis_update_abc import OnGuildEmojisUpdateABC
from .on_guild_integrations_update_abc import OnGuildIntegrationsUpdateABC
from .on_guild_join_abc import OnGuildJoinABC
from .on_guild_remove_abc import OnGuildRemoveABC
from .on_guild_role_create_abc import OnGuildRoleCreateABC
from .on_guild_role_delete_abc import OnGuildRoleDeleteABC
from .on_guild_role_update_abc import OnGuildRoleUpdateABC
from .on_guild_unavailable_abc import OnGuildUnavailableABC
from .on_guild_update_abc import OnGuildUpdateABC
from .on_invite_create_abc import OnInviteCreateABC
from .on_invite_delete_abc import OnInviteDeleteABC
from .on_member_ban_abc import OnMemberBanABC
from .on_member_join_abc import OnMemberJoinABC
from .on_member_remove_abc import OnMemberRemoveABC
from .on_member_unban_abc import OnMemberUnbanABC
from .on_member_update_abc import OnMemberUpdateABC
from .on_message_abc import OnMessageABC
from .on_message_delete_abc import OnMessageDeleteABC
from .on_message_edit_abc import OnMessageEditABC
from .on_private_channel_create_abc import OnPrivateChannelCreateABC
from .on_private_channel_delete_abc import OnPrivateChannelDeleteABC
from .on_private_channel_pins_update_abc import OnPrivateChannelPinsUpdateABC
from .on_private_channel_update_abc import OnPrivateChannelUpdateABC
from .on_reaction_add_abc import OnReactionAddABC
from .on_reaction_clear_abc import OnReactionClearABC
from .on_reaction_clear_emoji_abc import OnReactionClearEmojiABC
from .on_reaction_remove_abc import OnReactionRemoveABC
from .on_ready_abc import OnReadyABC
from .on_relationship_add_abc import OnRelationshipAddABC
from .on_relationship_remove_abc import OnRelationshipRemoveABC
from .on_relationship_update_abc import OnRelationshipUpdateABC
from .on_resume_abc import OnResumeABC
from .on_typing_abc import OnTypingABC
from .on_user_update_abc import OnUserUpdateABC
from .on_voice_state_update_abc import OnVoiceStateUpdateABC
from .on_webhooks_update_abc import OnWebhooksUpdateABC

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2022', minor='7', micro='0.post4')
