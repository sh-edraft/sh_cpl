# -*- coding: utf-8 -*-

"""
cpl-query CPL Queries
~~~~~~~~~~~~~~~~~~~

CPL Python integrated Queries

:copyright: (c) 2021 - 2023 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = "cpl_query.enumerable"
__author__ = "Sven Heidemann"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2021 - 2023 sh-edraft.de"
__version__ = "2023.2.0"

from collections import namedtuple


# imports:
from .enumerable import Enumerable
from .enumerable_abc import EnumerableABC

VersionInfo = namedtuple("VersionInfo", "major minor micro")
version_info = VersionInfo(major="2023", minor="2", micro="0")
