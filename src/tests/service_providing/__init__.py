# -*- coding: utf-8 -*-

"""
tests.service_providing 
~~~~~~~~~~~~~~~~~~~



:copyright: (c) 2020 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'tests.service_providing'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 sh-edraft.de'
__version__ = '2020.12.9'

from collections import namedtuple

# imports:

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major=2020, minor=12, micro=9)
