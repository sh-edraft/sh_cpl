# -*- coding: utf-8 -*-

"""
cpl-translation CPL Translation
~~~~~~~~~~~~~~~~~~~

CPL translation extension

:copyright: (c) 2022 - 2023 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = "cpl_translation"
__author__ = "Sven Heidemann"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2022 - 2023 sh-edraft.de"
__version__ = "2023.4.0.post1"

from collections import namedtuple


# imports:
from .translate_pipe import TranslatePipe
from .translation_service import TranslationService
from .translation_service_abc import TranslationServiceABC
from .translation_settings import TranslationSettings

# build-ignore


def add_translation(self):
    from cpl_core.console import Console
    from cpl_core.pipes import PipeABC
    from cpl_translation.translate_pipe import TranslatePipe
    from cpl_translation.translation_service import TranslationService
    from cpl_translation.translation_service_abc import TranslationServiceABC

    try:
        self.add_singleton(TranslationServiceABC, TranslationService)
        self.add_transient(PipeABC, TranslatePipe)
    except ImportError as e:
        Console.error("cpl-translation is not installed", str(e))


def init():
    from cpl_core.dependency_injection import ServiceCollection

    ServiceCollection.add_translation = add_translation


init()
# build-ignore-end

VersionInfo = namedtuple("VersionInfo", "major minor micro")
version_info = VersionInfo(major="2023", minor="4", micro="0.post1")
