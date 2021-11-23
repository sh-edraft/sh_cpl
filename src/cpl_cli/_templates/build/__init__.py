# -*- coding: utf-8 -*-

"""
sh_cpl-cli sh-edraft Common Python library CLI
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library Command Line Interface

:copyright: (c) 2020 - 2021 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_cli._templates.build'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 - 2021 sh-edraft.de'
__version__ = '2021.10.3.post2'

from collections import namedtuple

# imports:

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2021', minor='10', micro='3.post2')
