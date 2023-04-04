# -*- coding: utf-8 -*-

"""
cpl-core CPL core
~~~~~~~~~~~~~~~~~~~

CPL core package

:copyright: (c) 2020 - 2023 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_core.application'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 - 2023 sh-edraft.de'
__version__ = '2023.4.0'

from collections import namedtuple


# imports:
from .application_abc import ApplicationABC
from .application_builder import ApplicationBuilder
from .application_builder_abc import ApplicationBuilderABC
from .application_extension_abc import ApplicationExtensionABC
from .startup_abc import StartupABC
from .startup_extension_abc import StartupExtensionABC

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2023', minor='4', micro='0')
