# -*- coding: utf-8 -*-

"""
cpl-core CPL core
~~~~~~~~~~~~~~~~~~~

CPL core package

:copyright: (c) 2020 - 2024 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = "cpl_core.database.context"
__author__ = "Sven Heidemann"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2020 - 2024 sh-edraft.de"
__version__ = "2024.6.0"

from collections import namedtuple


# imports:
from .database_context import DatabaseContext
from .database_context_abc import DatabaseContextABC

VersionInfo = namedtuple("VersionInfo", "major minor micro")
version_info = VersionInfo(major="2024", minor="6", micro="0")
