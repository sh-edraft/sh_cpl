# -*- coding: utf-8 -*-

"""
sh_cpl-core sh-edraft Common Python library
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library

:copyright: (c) 2020 - 2021 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_core.environment'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 - 2021 sh-edraft.de'
__version__ = '2021.11.0.post5'

from collections import namedtuple

# imports:
from .application_environment_abc import ApplicationEnvironmentABC
from .environment_name_enum import EnvironmentNameEnum
from .application_environment import ApplicationEnvironment

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2021', minor='11', micro='0.post5')
