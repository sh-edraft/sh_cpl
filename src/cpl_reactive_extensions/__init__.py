# -*- coding: utf-8 -*-

"""
cpl-reactive-extensions CPL Simple ReactiveX implementation
~~~~~~~~~~~~~~~~~~~

CPL Simple ReactiveX implementation, see RxJS and RxPy for detailed implementation.

:copyright: (c) 2023 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = "cpl_reactive_extensions"
__author__ = "Sven Heidemann"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2023 sh-edraft.de"
__version__ = "2023.4.dev170"

from collections import namedtuple

# imports
from .behavior_subject import BehaviorSubject
from .interval import Interval
from .observable import Observable
from .subject import Subject
from .subscriber import Subscriber
from .subscription import Subscription
from .type import ObserverOrCallable

VersionInfo = namedtuple("VersionInfo", "major minor micro")
version_info = VersionInfo(major="2023", minor="4", micro="dev170")
