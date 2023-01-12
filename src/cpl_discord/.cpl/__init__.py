# -*- coding: utf-8 -*-

"""
cpl-discord sh-edraft Common Python library Discord
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library link between discord.py and CPL

:copyright: (c) 2022 - 2023 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_discord'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2022 - 2023 sh-edraft.de'
__version__ = '2022.12.1.post1'

from collections import namedtuple


# imports:

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2022', minor='12', micro='1.post1')
