from cpl_core.application import ApplicationABC
from cpl_core.configuration import ConfigurationABC
from cpl_core.console import Console
from cpl_core.dependency_injection import ServiceProviderABC
from cpl_core.logging import LoggerABC
from cpl_discord.application.discord_bot_abc import DiscordBotApplicationABC
from cpl_discord.configuration.discord_bot_settings import DiscordBotSettings
from cpl_discord.service.discord_bot_service import DiscordBotService
from cpl_discord.service.discord_bot_service_abc import DiscordBotServiceABC


class Application(DiscordBotApplicationABC):

    def __init__(self, config: ConfigurationABC, services: ServiceProviderABC):
        ApplicationABC.__init__(self, config, services)

        self._bot: DiscordBotServiceABC = services.get_service(DiscordBotServiceABC)
        self._logger: LoggerABC = services.get_service(LoggerABC)
        self._bot_settings: DiscordBotSettings = config.get_configuration(DiscordBotSettings)

    async def configure(self):
        pass

    async def main(self):
        try:
            self._logger.debug(__name__, f'Starting...\n')
            self._logger.trace(__name__, f'Try to start {DiscordBotService.__name__}')
            await self._bot.start_async()
        except Exception as e:
            self._logger.error(__name__, 'Start failed', e)

    async def stop_async(self):
        try:
            self._logger.trace(__name__, f'Try to stop {DiscordBotService.__name__}')
            await self._bot.close()
            self._logger.trace(__name__, f'Stopped {DiscordBotService.__name__}')
        except Exception as e:
            self._logger.error(__name__, 'stop failed', e)

        Console.write_line()
