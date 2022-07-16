import traceback
from typing import Optional

from cpl_core.configuration.configuration_model_abc import ConfigurationModelABC
from cpl_core.console.console import Console
from cpl_cli.cli_settings_name_enum import CLISettingsNameEnum


class CLISettings(ConfigurationModelABC):

    def __init__(self):
        ConfigurationModelABC.__init__(self)

        self._pip_path: Optional[str] = None

    @property
    def pip_path(self) -> str:
        return self._pip_path

    def from_dict(self, settings: dict):
        try:
            self._pip_path = settings[CLISettingsNameEnum.pip_path.value]
        except Exception as e:
            Console.error(f'[ ERROR ] [ {__name__} ]: Reading error in {type(self).__name__} settings')
            Console.error(f'[ EXCEPTION ] [ {__name__} ]: {e} -> {traceback.format_exc()}')
