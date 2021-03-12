# -*- coding: utf-8 -*-

"""
sh_cpl sh-edraft Common Python library
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library

:copyright: (c) 2020 - 2021 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl.environment'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 - 2021 sh-edraft.de'
__version__ = '2021.4.1'

from collections import namedtuple

# imports:
from .environment_abc import EnvironmentABC
from .environment_name_enum import EnvironmentNameEnum
from .hosting_environment import HostingEnvironment

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major=2021, minor=4, micro=1)
