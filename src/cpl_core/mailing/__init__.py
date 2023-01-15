# -*- coding: utf-8 -*-

"""
cpl-core sh-edraft Common Python library
~~~~~~~~~~~~~~~~~~~

sh-edraft Common Python library

:copyright: (c) 2020 - 2023 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = 'cpl_core.mailing'
__author__ = 'Sven Heidemann'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2020 - 2023 sh-edraft.de'
__version__ = '2022.12.1.post3'

from collections import namedtuple


# imports:
from .email import EMail
from .email_client_service import EMailClient
from .email_client_abc import EMailClientABC
from .email_client_settings import EMailClientSettings
from .email_client_settings_name_enum import EMailClientSettingsNameEnum

VersionInfo = namedtuple('VersionInfo', 'major minor micro')
version_info = VersionInfo(major='2022', minor='12', micro='1.post3')
