# -*- coding: utf-8 -*-

"""
cpl-discord CPL Discord
~~~~~~~~~~~~~~~~~~~

Link between discord.py and CPL

:copyright: (c) 2022 - 2023 sh-edraft.de
:license: MIT, see LICENSE for more details.

"""

__title__ = "cpl_discord"
__author__ = "Sven Heidemann"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2022 - 2023 sh-edraft.de"
__version__ = "2023.4.0.post2"

from collections import namedtuple


# imports
# build-ignore


def add_discord(self):
    from cpl_core.console import Console
    from cpl_discord.service.discord_bot_service_abc import DiscordBotServiceABC
    from cpl_discord.service.discord_bot_service import DiscordBotService
    from cpl_discord.service.discord_service_abc import DiscordServiceABC
    from cpl_discord.service.discord_service import DiscordService

    try:
        self.add_singleton(DiscordServiceABC, DiscordService)
        self.add_singleton(DiscordBotServiceABC, DiscordBotService)
    except ImportError as e:
        Console.error("cpl-discord is not installed", str(e))


def init():
    from cpl_core.dependency_injection import ServiceCollection

    ServiceCollection.add_discord = add_discord


init()


def get_discord_collection(services: "ServiceCollectionABC") -> "DiscordCollectionABC":
    from cpl_discord.service.discord_collection import DiscordCollection
    from cpl_discord.service.discord_collection_abc import DiscordCollectionABC

    collection = DiscordCollection(services)
    services.add_singleton(DiscordCollectionABC, collection)
    return collection


# build-ignore-end

VersionInfo = namedtuple("VersionInfo", "major minor micro")
version_info = VersionInfo(major="2023", minor="4", micro="0.post2")
