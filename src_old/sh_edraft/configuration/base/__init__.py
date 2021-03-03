# -*- coding: utf-8 -*-

"""
sh_edraft.configuration.base 
~~~~~~~~~~~~~~~~~~~



:copyright: (c) 2020 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'sh_edraft.configuration.base'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 sh-edraft.de'
__version__ = '2020.12.9'

from collections import namedtuple

# imports:
from .configuration_base import ConfigurationBase
from .configuration_model_base import ConfigurationModelBase

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major=2020, minor=12, micro=9)
