# -*- coding: utf-8 -*-

"""
sh_cpl-core sh-edraft Common Python library
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library

:copyright: (c) 2020 - 2021 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_core.database'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 - 2021 sh-edraft.de'
__version__ = '2021.10.6'

from collections import namedtuple

# imports:
from .database_model import DatabaseModel
from .database_settings import DatabaseSettings
from .database_settings_name_enum import DatabaseSettingsNameEnum

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2021', minor='10', micro='6')
