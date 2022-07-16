import sys

import discord
from discord.ext import commands

from cpl_core.configuration import ConfigurationABC
from cpl_core.console import Console
from cpl_core.environment import ApplicationEnvironmentABC
from cpl_core.logging import LoggerABC, LoggingSettings, LoggingLevelEnum
from cpl_discord.configuration.discord_bot_settings import DiscordBotSettings
from cpl_discord.service.discord_bot_service_abc import DiscordBotServiceABC
from cpl_discord.service.discord_service_abc import DiscordServiceABC


class DiscordBotService(DiscordBotServiceABC):

    def __init__(
            self,
            config: ConfigurationABC,
            logger: LoggerABC,
            discord_bot_settings: DiscordBotSettings,
            env: ApplicationEnvironmentABC,
            logging_st: LoggingSettings,
            discord_service: DiscordServiceABC
    ):
        # services
        self._logger = logger
        self._env = env
        self._logging_st = logging_st
        self._discord_service = discord_service

        # settings
        if discord_bot_settings is None:
            self._discord_settings = DiscordBotSettings()
            token = config.get_configuration('TOKEN')
            if token is None:
                raise Exception('You have to configure discord token by appsettings or environment variables')

            prefix = config.get_configuration('PREFIX')
            self._discord_settings.from_dict({
                'Token': token,
                'Prefix': prefix if prefix is not None else '! '
            })
        else:
            self._discord_settings = discord_bot_settings

        # setup super
        DiscordBotServiceABC.__init__(self, command_prefix=self._discord_settings.prefix, help_command=None, intents=discord.Intents().all())

    async def start_async(self):
        self._logger.trace(__name__, 'Try to connect to discord')
        await self.start(self._discord_settings.token)
        # continue at on_ready

    async def stop_async(self):
        self._logger.trace(__name__, 'Try to disconnect from discord')
        try:
            await self.close()
        except Exception as e:
            self._logger.error(__name__, 'Stop failed', e)

    async def on_ready(self):
        self._logger.info(__name__, 'Connected to discord')

        self._logger.header(f'{self.user.name}:')
        if self._logging_st.console.value >= LoggingLevelEnum.INFO.value:
            Console.banner(self._env.application_name if self._env.application_name != '' else 'A bot')

        self.add_cog(self._discord_service)

        await self._discord_service.on_ready()
