import discord

from cpl_core.configuration import ConfigurationABC
from cpl_core.console import Console
from cpl_core.environment import ApplicationEnvironmentABC
from cpl_core.logging import LoggerABC, LoggingSettings, LoggingLevelEnum
from cpl_discord.configuration.discord_bot_settings import DiscordBotSettings
from cpl_discord.container.guild import Guild
from cpl_discord.helper.to_containers_converter import ToContainersConverter
from cpl_discord.service.discord_bot_service_abc import DiscordBotServiceABC
from cpl_discord.service.discord_service_abc import DiscordServiceABC
from cpl_query.extension.list import List


class DiscordBotService(DiscordBotServiceABC):

    def __init__(
            self,
            config: ConfigurationABC,
            logger: LoggerABC,
            discord_bot_settings: DiscordBotSettings,
            env: ApplicationEnvironmentABC,
            logging_st: LoggingSettings,
            discord_service: DiscordServiceABC,
            *args,
            **kwargs
    ):
        # services
        self._config = config
        self._logger = logger
        self._env = env
        self._logging_st = logging_st
        self._discord_service = discord_service

        # settings
        self._discord_settings = self._get_settings(discord_bot_settings)

        # setup super
        DiscordBotServiceABC.__init__(
            self,
            *args,
            command_prefix=self._discord_settings.prefix, help_command=None, intents=discord.Intents().all(),
            **kwargs
        )
        self._base = super(DiscordBotServiceABC, self)

    @staticmethod
    def _is_string_invalid(x):
        return x is None or x == ''

    def _get_settings(self, settings_from_config: DiscordBotSettings) -> DiscordBotSettings:
        new_settings = DiscordBotSettings()
        token = None if settings_from_config is None else settings_from_config.token
        prefix = None if settings_from_config is None else settings_from_config.prefix
        env_token = self._config.get_configuration('TOKEN')
        env_prefix = self._config.get_configuration('PREFIX')

        new_settings.from_dict({
            'Token': env_token if token is None or token == '' else token,
            'Prefix':
                ('! ' if self._is_string_invalid(env_prefix) else env_prefix)
                if self._is_string_invalid(prefix) else prefix
        })
        if new_settings.token is None or new_settings.token == '':
            raise Exception('You have to configure discord token by appsettings or environment variables')
        return new_settings

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

        await self._discord_service.init(self)
        await self.wait_until_ready()
        await self.tree.sync()
        self._logger.debug(__name__, f'Finished syncing commands')

        await self._discord_service.on_ready()

    @property
    def guilds(self) -> List[Guild]:
        return List(Guild, ToContainersConverter.convert(self._base.guilds, Guild))
