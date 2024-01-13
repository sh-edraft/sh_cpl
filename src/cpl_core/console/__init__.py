# -*- coding: utf-8 -*-

"""
cpl-core CPL core
~~~~~~~~~~~~~~~~~~~

CPL core package

:copyright: (c) 2020 - 2024 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = "cpl_core.console"
__author__ = "Sven Heidemann"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2020 - 2024 sh-edraft.de"
__version__ = "2023.10.2"

from collections import namedtuple


# imports:
from .background_color_enum import BackgroundColorEnum
from .console import Console
from .console_call import ConsoleCall
from .foreground_color_enum import ForegroundColorEnum
from .spinner_thread import SpinnerThread

VersionInfo = namedtuple("VersionInfo", "major minor micro")
version_info = VersionInfo(major="2023", minor="10", micro="2")
