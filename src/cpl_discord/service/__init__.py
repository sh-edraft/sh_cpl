# -*- coding: utf-8 -*-

"""
cpl-discord CPL Discord
~~~~~~~~~~~~~~~~~~~

Link between discord.py and CPL

:copyright: (c) 2022 - 2023 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_discord.service'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2022 - 2023 sh-edraft.de'
__version__ = '2023.4.0'

from collections import namedtuple


# imports:
from .command_error_handler_service import CommandErrorHandlerService
from .discord_bot_service import DiscordBotService
from .discord_bot_service_abc import DiscordBotServiceABC
from .discord_collection import DiscordCollection
from .discord_service import DiscordService
from .discord_service_abc import DiscordServiceABC

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2023', minor='4', micro='0')
