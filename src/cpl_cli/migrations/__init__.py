# -*- coding: utf-8 -*-

"""
cpl-cli sh-edraft Common Python library CLI
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library Command Line Interface

:copyright: (c) 2020 - 2023 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_cli.migrations'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 - 2023 sh-edraft.de'
__version__ = '2022.12.1.post2'

from collections import namedtuple


# imports

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2022', minor='12', micro='1.post2')
