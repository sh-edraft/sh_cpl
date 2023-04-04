# -*- coding: utf-8 -*-

"""
cpl-query CPL Queries
~~~~~~~~~~~~~~~~~~~

CPL Python integrated Queries

:copyright: (c) 2021 - 2023 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_query'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2021 - 2023 sh-edraft.de'
__version__ = '2023.4.0'

from collections import namedtuple


# imports:

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2023', minor='4', micro='0')
