# -*- coding: utf-8 -*-

"""
cpl-discord sh-edraft Common Python library Discord
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library link between discord.py and CPL

:copyright: (c) 2021 - 2022 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_discord.command'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2021 - 2022 sh-edraft.de'
__version__ = '2022.7.0.post1'

from collections import namedtuple


# imports:
from .discord_command_abc import DiscordCommandABC
from .discord_commands_meta import DiscordCogMeta

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2022', minor='7', micro='0.post1')
