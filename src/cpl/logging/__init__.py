# -*- coding: utf-8 -*-

"""
sh_cpl sh-edraft Common Python library
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library

:copyright: (c) 2020 - 2021 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl.logging'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 - 2021 sh-edraft.de'
__version__ = '2021.4.2.dev1'

from collections import namedtuple

# imports:
from .logger_service import Logger
from .logger_abc import LoggerABC
from .logging_level_enum import LoggingLevelEnum
from .logging_settings import LoggingSettings
from .logging_settings_name_enum import LoggingSettingsNameEnum

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2021', minor='04', micro='02.dev1')
