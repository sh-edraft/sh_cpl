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
        Console.error('cpl-discord is not installed', str(e))


def init():
    from cpl_core.dependency_injection import ServiceCollection
    ServiceCollection.add_discord = add_discord


init()


def get_discord_collection(services: 'ServiceCollectionABC') -> 'DiscordCollectionABC':
    from cpl_discord.service.discord_collection import DiscordCollection
    from cpl_discord.service.discord_collection_abc import DiscordCollectionABC
    collection = DiscordCollection(services)
    services.add_singleton(DiscordCollectionABC, collection)
    return collection
# build-ignore-end
