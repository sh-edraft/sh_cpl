# -*- coding: utf-8 -*-

"""
sh_edraft common python library
~~~~~~~~~~~~~~~~~~~

Library to share common classes and models used at sh-edraft.de

:copyright: (c) 2020 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'sh_edraft'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 sh-edraft.de'
__version__ = '2020.12.5'

from collections import namedtuple

# imports:

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major=2020, minor=12, micro=5)
