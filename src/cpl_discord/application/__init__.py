# -*- coding: utf-8 -*-

"""
cpl-discord CPL Discord
~~~~~~~~~~~~~~~~~~~

Link between discord.py and CPL

:copyright: (c) 2022 - 2023 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = "cpl_discord.application"
__author__ = "Sven Heidemann"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2022 - 2023 sh-edraft.de"
__version__ = "2023.4.0.post2"

from collections import namedtuple


# imports
from .discord_bot_application_abc import DiscordBotApplicationABC

VersionInfo = namedtuple("VersionInfo", "major minor micro")
version_info = VersionInfo(major="2023", minor="4", micro="0.post2")
