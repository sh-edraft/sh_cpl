# -*- coding: utf-8 -*-

"""
cpl-core CPL core
~~~~~~~~~~~~~~~~~~~

CPL core package

:copyright: (c) 2020 - 2024 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = "cpl_core.environment"
__author__ = "Sven Heidemann"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2020 - 2024 sh-edraft.de"
__version__ = "2024.6.0"

from collections import namedtuple


# imports:
from .application_environment_abc import ApplicationEnvironmentABC
from .environment_name_enum import EnvironmentNameEnum
from .application_environment import ApplicationEnvironment

VersionInfo = namedtuple("VersionInfo", "major minor micro")
version_info = VersionInfo(major="2024", minor="6", micro="0")
