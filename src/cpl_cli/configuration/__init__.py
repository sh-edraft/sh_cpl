# -*- coding: utf-8 -*-

"""
sh_cpl sh-edraft Common Python library
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library

:copyright: (c) 2020 - 2021 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_cli.configuration'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 - 2021 sh-edraft.de'
__version__ = '2021.4.1'

from collections import namedtuple

# imports:
from .build_settings import BuildSettings
from .build_settings_name_enum import BuildSettingsNameEnum
from .project_settings import ProjectSettings
from .project_settings_name_enum import ProjectSettingsNameEnum
from .version_settings import VersionSettings
from .version_settings_name_enum import VersionSettingsNameEnum

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2021', minor='04', micro='01')
