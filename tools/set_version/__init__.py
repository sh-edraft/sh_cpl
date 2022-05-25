# -*- coding: utf-8 -*-

"""
set-version CPL internal tool to set version from branch name
~~~~~~~~~~~~~~~~~~~

CPL internal tool to set version from branch name

:copyright: (c) 2022 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'set_version'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2022 sh-edraft.de'
__version__ = '2022.6.0'

from collections import namedtuple

# imports: 

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2022', minor='6', micro='0')
