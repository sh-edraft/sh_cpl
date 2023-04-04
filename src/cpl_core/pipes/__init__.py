# -*- coding: utf-8 -*-

"""
cpl-core CPL core
~~~~~~~~~~~~~~~~~~~

CPL core package

:copyright: (c) 2020 - 2023 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_core.pipes'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 - 2023 sh-edraft.de'
__version__ = '2023.4.0'

from collections import namedtuple


# imports:
from .bool_pipe import BoolPipe
from .first_char_to_lower_pipe import FirstCharToLowerPipe
from .first_to_upper_pipe import FirstToUpperPipe
from .ip_address_pipe import IPAddressPipe
from .pipe_abc import PipeABC
from .to_camel_case_pipe import ToCamelCasePipe
from .to_snake_case_pipe import ToSnakeCasePipe

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2023', minor='4', micro='0')
