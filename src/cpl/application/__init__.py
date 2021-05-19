# -*- coding: utf-8 -*-

"""
sh_cpl sh-edraft Common Python library
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library

:copyright: (c) 2020 - 2021 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl.application'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 - 2021 sh-edraft.de'
__version__ = '2021.4.0.post1'

from collections import namedtuple

# imports:
from .application_abc import ApplicationABC
from .application_builder import ApplicationBuilder
from .application_builder_abc import ApplicationBuilderABC
from .startup_abc import StartupABC

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2021', minor='4', micro='0.post1')