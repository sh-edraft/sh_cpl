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
__version__ = '2021.4.post1'

from collections import namedtuple

# imports:
from .service_collection import ServiceCollection
from .service_collection_abc import ServiceCollectionABC
from .service_descriptor import ServiceDescriptor
from .service_lifetime_enum import ServiceLifetimeEnum
from .service_provider import ServiceProvider
from .service_provider_abc import ServiceProviderABC

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2021', minor='4', micro='post1')
