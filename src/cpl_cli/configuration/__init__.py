# -*- coding: utf-8 -*-

"""
cpl-cli CPL CLI
~~~~~~~~~~~~~~~~~~~

CPL Command Line Interface

:copyright: (c) 2020 - 2023 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = "cpl_cli.configuration"
__author__ = "Sven Heidemann"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2020 - 2023 sh-edraft.de"
__version__ = "2023.4.0.post3"

from collections import namedtuple


# imports:
from .build_settings import BuildSettings
from .build_settings_name_enum import BuildSettingsNameEnum
from .project_settings import ProjectSettings
from .project_settings_name_enum import ProjectSettingsNameEnum
from .version_settings import VersionSettings
from .version_settings_name_enum import VersionSettingsNameEnum
from .workspace_settings import WorkspaceSettings
from .workspace_settings_name_enum import WorkspaceSettingsNameEnum

VersionInfo = namedtuple("VersionInfo", "major minor micro")
version_info = VersionInfo(major="2023", minor="4", micro="0.post3")
