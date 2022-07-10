# -*- coding: utf-8 -*-

"""
cpl-core sh-edraft Common Python library
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library

:copyright: (c) 2020 - 2022 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_core.dependency_injection'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 - 2022 sh-edraft.de'
__version__ = '2022.7.0'

from collections import namedtuple


# imports:
from .scope import Scope
from .scope_abc import ScopeABC
from .service_collection import ServiceCollection
from .service_collection_abc import ServiceCollectionABC
from .service_descriptor import ServiceDescriptor
from .service_lifetime_enum import ServiceLifetimeEnum
from .service_provider import ServiceProvider
from .service_provider_abc import ServiceProviderABC

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2022', minor='7', micro='0')
