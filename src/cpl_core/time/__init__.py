# -*- coding: utf-8 -*-

"""
cpl-core sh-edraft Common Python library
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library

:copyright: (c) 2020 - 2022 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_core.time'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 - 2022 sh-edraft.de'
__version__ = '2022.10.0'

from collections import namedtuple


# imports:
from .time_format_settings import TimeFormatSettings
from .time_format_settings_names_enum import TimeFormatSettingsNamesEnum

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2022', minor='10', micro='0')
