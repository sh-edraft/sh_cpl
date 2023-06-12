# -*- coding: utf-8 -*-

"""
cpl-cli CPL CLI
~~~~~~~~~~~~~~~~~~~

CPL Command Line Interface

:copyright: (c) 2020 - 2023 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = "cpl_cli"
__author__ = "Sven Heidemann"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2020 - 2023 sh-edraft.de"
__version__ = "2023.4.0.post1"

from collections import namedtuple


# imports:
from .cli import CLI
from .command_abc import CommandABC
from .error import Error
from .main import main
from .startup import Startup

VersionInfo = namedtuple("VersionInfo", "major minor micro")
version_info = VersionInfo(major="2023", minor="4", micro="0.post1")
