# -*- coding: utf-8 -*-

"""
cpl-query sh-edraft Common Python library Query
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library Python integrated Queries

:copyright: (c) 2020 - 2022 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_query._query'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 - 2022 sh-edraft.de'
__version__ = '2021.6.1'

from collections import namedtuple

# imports:

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2021', minor='6', micro='1')
