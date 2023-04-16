# -*- coding: utf-8 -*-

"""
cpl-reactive-extensions CPL Simple ReactiveX implementation
~~~~~~~~~~~~~~~~~~~

CPL Simple ReactiveX implementation, see RxJS and RxPy for detailed implementation.

:copyright: (c) 2023 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = "cpl_reactive_extensions.scheduler"
__author__ = "Sven Heidemann"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2023 sh-edraft.de"
__version__ = "2023.4.dev170"

from collections import namedtuple


# imports:

VersionInfo = namedtuple("VersionInfo", "major minor micro")
version_info = VersionInfo(major="2023", minor="4", micro="dev170")
