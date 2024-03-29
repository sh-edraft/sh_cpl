# -*- coding: utf-8 -*-

"""
general sh-edraft Common Python library
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library

:copyright: (c) 2020 - 2021 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = "general.arguments"
__author__ = "Sven Heidemann"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2020 - 2021 sh-edraft.de"
__version__ = "2021.4.1"

from collections import namedtuple


# imports:

VersionInfo = namedtuple("VersionInfo", "major minor micro")
version_info = VersionInfo(major="2021", minor="04", micro="01")
