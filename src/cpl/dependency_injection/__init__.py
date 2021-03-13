# -*- coding: utf-8 -*-

"""
sh_cpl sh-edraft Common Python library
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library

:copyright: (c) 2020 - 2021 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl.dependency_injection'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 - 2021 sh-edraft.de'
__version__ = '2021.04.01'

from collections import namedtuple

# imports:
from .service_abc import ServiceABC
from .service_provider import ServiceProvider
from .service_provider_abc import ServiceProviderABC

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2021', minor='04', micro='01')
