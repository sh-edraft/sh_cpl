from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC


class DiscordBotSettings(ConfigurationModelABC):
    def __init__(
        self,
        token: str = None,
        prefix: str = None,
    ):
        ConfigurationModelABC.__init__(self)

        self._token = token
        self._prefix = prefix

    @property
    def token(self) -> str:
        return self._token

    @property
    def prefix(self) -> str:
        return self._prefix
