import traceback

from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC
from cpl_core.console import Console


class DiscordBotSettings(ConfigurationModelABC):

    def __init__(self):
        ConfigurationModelABC.__init__(self)

        self._token = ''
        self._prefix = ''

    @property
    def token(self) -> str:
        return self._token

    @property
    def prefix(self) -> str:
        return self._prefix

    def from_dict(self, settings: dict):
        try:
            self._token = settings['Token']
            self._prefix = settings['Prefix']
        except Exception as e:
            Console.error(f'[ ERROR ] [ {__name__} ]: Reading error in {__name__} settings')
            Console.error(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}')
