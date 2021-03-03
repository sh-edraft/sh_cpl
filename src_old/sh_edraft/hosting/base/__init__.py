# -*- coding: utf-8 -*-

"""
sh_edraft.hosting.base 
~~~~~~~~~~~~~~~~~~~



:copyright: (c) 2020 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'sh_edraft.hosting.base'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 sh-edraft.de'
__version__ = '2020.12.9'

from collections import namedtuple

# imports:
from .application_base import ApplicationBase
from .application_host_base import ApplicationHostBase
from .application_runtime_base import ApplicationRuntimeBase

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major=2020, minor=12, micro=9)
