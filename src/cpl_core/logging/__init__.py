# -*- coding: utf-8 -*-

"""
cpl-core CPL core
~~~~~~~~~~~~~~~~~~~

CPL core package

:copyright: (c) 2020 - 2023 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_core.logging'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 - 2023 sh-edraft.de'
__version__ = '2023.10.1'

from collections import namedtuple


# imports:
from .logger_service import Logger
from .logger_abc import LoggerABC
from .logging_level_enum import LoggingLevelEnum
from .logging_settings import LoggingSettings
from .logging_settings_name_enum import LoggingSettingsNameEnum

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2023', minor='10', micro='1')
