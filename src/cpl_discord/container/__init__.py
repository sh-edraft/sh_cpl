# -*- coding: utf-8 -*-

"""
cpl-discord CPL Discord
~~~~~~~~~~~~~~~~~~~

Link between discord.py and CPL

:copyright: (c) 2022 - 2023 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_discord.container'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2022 - 2023 sh-edraft.de'
__version__ = '2023.4.0'

from collections import namedtuple


# imports
from .category_channel import CategoryChannel
from .container import Container
from .guild import Guild
from .member import Member
from .role import Role
from .text_channel import TextChannel
from .thread import Thread
from .voice_channel import VoiceChannel

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2023', minor='4', micro='0')
