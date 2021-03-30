# -*- coding: utf-8 -*-

"""
sh_cpl sh-edraft Common Python library
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library

:copyright: (c) 2020 - 2021 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl.configuration'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 - 2021 sh-edraft.de'
__version__ = '2021.4.0rc2'

from collections import namedtuple

# imports:
from .configuration import Configuration
from .configuration_abc import ConfigurationABC
from .configuration_model_abc import ConfigurationModelABC
from .configuration_variable_name_enum import ConfigurationVariableNameEnum
from .console_argument import ConsoleArgument

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2021', minor='04', micro='0rc2')
