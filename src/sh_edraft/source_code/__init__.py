# -*- coding: utf-8 -*-

"""
sh_edraft.source_code 
~~~~~~~~~~~~~~~~~~~



:copyright: (c) 2020 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'sh_edraft.source_code'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 sh-edraft.de'
__version__ = '2020.12.0.1'

from collections import namedtuple



VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major=2020, minor=12, micro=0.1)
