# -*- coding: utf-8 -*-

"""
cpl-cli sh-edraft Common Python library CLI
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library Command Line Interface

:copyright: (c) 2020 - 2022 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_cli.publish'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 - 2022 sh-edraft.de'
__version__ = '2022.6.15.dev2'

from collections import namedtuple

# imports:
from .publisher_abc import PublisherABC
from .publisher_service import PublisherService

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2022', minor='6', micro='15.dev2')
