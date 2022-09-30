# -*- coding: utf-8 -*-

"""
cpl-query sh-edraft Common Python library Query
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library Python integrated Queries

:copyright: (c) 2021 - 2022 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_query.iterable'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2021 - 2022 sh-edraft.de'
__version__ = '2022.10.0'

from collections import namedtuple


# imports:
from .iterable_abc import IterableABC
from .iterable import Iterable
from .ordered_iterable_abc import OrderedIterableABC
from .ordered_iterable import OrderedIterable

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2022', minor='10', micro='0')
