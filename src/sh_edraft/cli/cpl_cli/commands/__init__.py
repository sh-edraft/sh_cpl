# -*- coding: utf-8 -*-

"""
sh_edraft.cli.cpl_cli.commands 
~~~~~~~~~~~~~~~~~~~



:copyright: (c) 2020 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'sh_edraft.cli.cpl_cli.commands'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 sh-edraft.de'
__version__ = '2020.12.10'

from collections import namedtuple

# imports:
from .version import Version
from .help import Help
from .new import New

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major=2020, minor=12, micro=10)
