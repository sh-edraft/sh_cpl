# -*- coding: utf-8 -*-

"""
cpl-core CPL core
~~~~~~~~~~~~~~~~~~~

CPL core package

:copyright: (c) 2020 - 2024 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = "cpl_core.configuration"
__author__ = "Sven Heidemann"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2020 - 2024 sh-edraft.de"
__version__ = "2024.6.0"

from collections import namedtuple


# imports:
from .argument_abc import ArgumentABC
from .argument_builder import ArgumentBuilder
from .argument_executable_abc import ArgumentExecutableABC
from .argument_type_enum import ArgumentTypeEnum
from .configuration import Configuration
from .configuration_abc import ConfigurationABC
from .configuration_model_abc import ConfigurationModelABC
from .configuration_variable_name_enum import ConfigurationVariableNameEnum
from .executable_argument import ExecutableArgument
from .flag_argument import FlagArgument
from .validator_abc import ValidatorABC
from .variable_argument import VariableArgument

VersionInfo = namedtuple("VersionInfo", "major minor micro")
version_info = VersionInfo(major="2024", minor="6", micro="0")
