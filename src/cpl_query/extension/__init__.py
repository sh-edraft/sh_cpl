# -*- coding: utf-8 -*-

"""
sh_cpl_query sh-edraft Common Python library Query
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library Python integrated Queries

:copyright: (c) 2020 - 2021 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_query.extension'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 - 2021 sh-edraft.de'
__version__ = '2021.10.3'

from collections import namedtuple

# imports:

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2021', minor='10', micro='3')
