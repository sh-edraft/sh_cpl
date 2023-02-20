# -*- coding: utf-8 -*-

"""
cpl-cli CPL CLI
~~~~~~~~~~~~~~~~~~~

CPL Command Line Interface

:copyright: (c) 2020 - 2023 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = "cpl_cli.command"
__author__ = "Sven Heidemann"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2020 - 2023 sh-edraft.de"
__version__ = "2023.2.0"

from collections import namedtuple


# imports:
from .build_service import BuildService
from .generate_service import GenerateService
from .help_service import HelpService
from .new_service import NewService
from .publish_service import PublishService
from .version_service import VersionService

VersionInfo = namedtuple("VersionInfo", "major minor micro")
version_info = VersionInfo(major="2023", minor="2", micro="0")
