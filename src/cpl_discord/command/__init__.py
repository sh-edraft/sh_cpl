# -*- coding: utf-8 -*-

"""
cpl-discord CPL Discord
~~~~~~~~~~~~~~~~~~~

Link between discord.py and CPL

:copyright: (c) 2022 - 2023 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = "cpl_discord.command"
__author__ = "Sven Heidemann"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2022 - 2023 sh-edraft.de"
__version__ = "2023.10.0"

from collections import namedtuple


# imports:
from .discord_command_abc import DiscordCommandABC
from .discord_commands_meta import DiscordCogMeta

VersionInfo = namedtuple("VersionInfo", "major minor micro")
version_info = VersionInfo(major="2023", minor="10", micro="0")
